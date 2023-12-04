#include "GStreamerHandler.hpp"
#include <gst/rtsp-server/rtsp-server.h>

GStreamerHandler::GStreamerHandler()
{
    gst_init(nullptr, nullptr);
    log.Info("Streaming initialized successfully!");
}

GStreamerHandler::~GStreamerHandler()
{
    this->Stop();

    if (streamingThread.joinable())
    {
        streamingThread.join();
    }

    if (this->streamLoop)
    {
        g_main_loop_unref(this->streamLoop);
    }

    gst_deinit();
    log.Info("Goodbye! (~˘▾˘)~");
}

gboolean GStreamerHandler::BusCallback(GstBus *bus, GstMessage *msg, gpointer data)
{
    auto handler = static_cast<GStreamerHandler*>(data);

    switch (GST_MESSAGE_TYPE(msg))
    {
        case GST_MESSAGE_ERROR: 
            GError *err;
            gchar *debug;

            gst_message_parse_error(msg, &err, &debug);
            handler->log.Error("GStreamer: " + std::string(err->message));

            g_error_free(err);
            g_free(debug);

            handler->Cleanup();
            break;

        case GST_MESSAGE_EOS:
            handler->log.Info("GStreamer: End of stream");
            handler->Cleanup();
            break;

        default:
            break;
    }

    return TRUE;
}

bool GStreamerHandler::IsPipelineValid(GstElement *pipeline, GError *&handle)
{
    if (handle)
    {
        log.Error("Failed to create pipeline: " + std::string(handle->message));
        return false;
    }

    if (!pipeline)
    {
        log.Error("Failed to create pipeline: Unknown error.");
        return false;
    }

    return true;
}

std::string GStreamerHandler::ParsePipeline(const std::string &ipAddress, const std::string &port)
{
    auto result = this->rawPipeline;
    
    auto addressPos = this->rawPipeline.find("{ADDRESS}");
    if (addressPos != std::string::npos)
    {
        result.replace(addressPos, sizeof("{ADDRESS}") - 1, ipAddress);
    }

    auto portPos = this->rawPipeline.find("{PORT}");
    if (portPos != std::string::npos)
    {
        result.replace(portPos, sizeof("{PORT}") - 1, port);
    }

    return result;
}

void GStreamerHandler::SetupStream()
{
    auto bus = gst_pipeline_get_bus(GST_PIPELINE(this->pipeline));
    gst_bus_add_watch(bus, this->BusCallback, this);
    gst_object_unref(bus);

    if (gst_element_set_state(this->pipeline, GST_STATE_PLAYING) == GST_STATE_CHANGE_FAILURE)
    {
        throw std::runtime_error("Failed to start pipeline!");
    }

    if (!this->streamLoop)
    {
        this->streamLoop = g_main_loop_new(NULL, FALSE);
    }
}

void GStreamerHandler::Cleanup()
{
    log.Debug("Starting Cleanup process...");

    if (this->pipeline)
    {
        log.Debug("Stopping GStreamer pipeline...");
        gst_element_set_state(this->pipeline, GST_STATE_NULL);
        gst_object_unref(GST_OBJECT(this->pipeline));
        this->pipeline = nullptr;
    }

    if (this->rtspServer)
    {
        log.Debug("Disconnecting RTSP server clients...");

        auto session_pool = gst_rtsp_server_get_session_pool(this->rtspServer);
        if (session_pool)
        {
            // Remove all sessions to force disconnect clients
            gst_rtsp_session_pool_cleanup(session_pool);
            g_object_unref(session_pool);
        }
        gst_rtsp_thread_pool_cleanup();

        g_object_unref(this->rtspServer);
        this->rtspServer = nullptr;
    }

    if (this->streamLoop)
    {
        if (g_main_loop_is_running(this->streamLoop))
        {
            log.Debug("Quitting main loop...");
            g_main_loop_quit(this->streamLoop);
        }
        g_main_loop_unref(this->streamLoop);
        this->streamLoop = nullptr;
    }

    if (this->mediaFactory)
    {
        log.Debug("Unreferencing media factory...");
        g_object_unref(this->mediaFactory);
        this->mediaFactory = nullptr;
    }

    log.Debug("Cleanup process completed.");
}


void GStreamerHandler::SetPipeline(const std::string &pipeline)
{
    this->rawPipeline = pipeline;
    log.Info("Pipeline set to: " + this->rawPipeline);
}

void GStreamerHandler::BuildPipeline(const std::string &ipAddress, const std::string &port, bool rtsp)
{
    if (streamingThread.joinable())
    {
        streamingThread.join();
    }

    if (rtsp)
    {
        if (!this->rtspServer)
        {
            this->rtspServer = gst_rtsp_server_new();
            this->mediaFactory = gst_rtsp_media_factory_new();

            gst_rtsp_server_set_address(this->rtspServer, ipAddress.c_str());
            gst_rtsp_server_set_service(this->rtspServer, port.c_str());

            gst_rtsp_media_factory_set_launch(this->mediaFactory, this->ParsePipeline(ipAddress, port).c_str());
            gst_rtsp_media_factory_set_shared(this->mediaFactory, TRUE);

            auto mounts = gst_rtsp_server_get_mount_points(this->rtspServer);
            gst_rtsp_mount_points_add_factory(mounts, "/stream", this->mediaFactory);
            g_object_unref(mounts);
        }
    }
    else
    {
        if (this->pipeline != nullptr)
        {
            gst_object_unref(GST_OBJECT(this->pipeline));
        }

        GError* errorHandle = nullptr;
        auto newPipeline = gst_parse_launch(this->ParsePipeline(ipAddress, port).c_str(), &errorHandle);

        if (IsPipelineValid(newPipeline, errorHandle))
        {
            this->pipeline = newPipeline;
        }
        else
        {
            log.Error("Failed to build pipeline!");
        }
    }
}

void GStreamerHandler::Start(bool rtsp)
{
    if (this->isStreaming.load())
    {
        log.Warning("Stream is already live!");
        return;
    }

    if (rtsp)
    {
        if (!this->rtspServer)
        {
            log.Error("RTSP Server is not set! Aborting.");
            return;
        }

        GError *error = nullptr;
        gst_rtsp_server_attach(this->rtspServer, NULL);
        this->streamLoop = g_main_loop_new(NULL, FALSE);
    }
    else
    {
        if (this->pipeline == nullptr)
        {
            log.Error("Pipeline is not set! Aborting.");
            return;
        }
    }
    
    this->streamingThread = std::thread([this, rtsp]()
    {
        try
        {
            if (!rtsp)
            {
                this->SetupStream();
            }

            this->isStreaming.store(true);
            g_main_loop_run(this->streamLoop);
        }
        catch (const std::exception& e)
        {
            log.Error(std::string(e.what()));
        }

        this->isStreaming.store(false);
    });
}

void GStreamerHandler::Stop()
{
    if (!this->isStreaming.load())
    {
        return;
    }

    this->Cleanup();

    if (streamingThread.joinable())
    {
        streamingThread.join();
    }
}

bool GStreamerHandler::IsStreaming()
{
    return isStreaming.load();
}
