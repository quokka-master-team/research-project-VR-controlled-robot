#include "GStreamerHandler.hpp"

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

void GStreamerHandler::Cleanup()
{
    if (this->pipeline)
    {
        gst_element_set_state(this->pipeline, GST_STATE_NULL);
        gst_object_unref(GST_OBJECT(this->pipeline));
        this->pipeline = nullptr;
    }

    if (this->streamLoop)
    {
        g_main_loop_quit(this->streamLoop);
        g_main_loop_unref(this->streamLoop);
        this->streamLoop = nullptr;
    }
}

void GStreamerHandler::SetPipeline(const std::string &pipeline)
{
    this->rawPipeline = pipeline;
    log.Info("Pipeline set to: " + this->rawPipeline);
}

void GStreamerHandler::BuildPipeline(const std::string &ipAddress, const std::string &port)
{
    auto pipeline = this->rawPipeline;
    
    auto addressPos = pipeline.find("{ADDRESS}");
    if (addressPos != std::string::npos)
    {
        pipeline.replace(addressPos, sizeof("{ADDRESS}") - 1, ipAddress);
    }

    auto portPos = pipeline.find("{PORT}");
    if (portPos != std::string::npos)
    {
        pipeline.replace(portPos, sizeof("{PORT}") - 1, port);
    }

    if (streamingThread.joinable())
    {
        streamingThread.join();
    }

    if (this->pipeline != nullptr)
    {
        gst_object_unref(GST_OBJECT(this->pipeline));
    }

    GError* errorHandle = nullptr;
    auto newPipeline = gst_parse_launch(pipeline.c_str(), &errorHandle);

    if (!IsPipelineValid(newPipeline, errorHandle))
    {
        log.Warning("Failed to load new pipeline. Reverting changes!");

        if (this->pipeline != nullptr)
        {
            gst_parse_launch(pipeline.c_str(), &errorHandle);
        }

        return;
    }
    else
    {
        log.Info("Pipeline '" + pipeline + "' loaded!");
    }

    this->pipeline = newPipeline;
}

void GStreamerHandler::Start()
{
    if (this->pipeline == nullptr)
    {
        log.Error("Pipeline is not set! Aborting.");
        return;
    }

    if (this->isStreaming.load())
    {
        log.Warning("Stream is already live!");
        return;
    }

    this->streamingThread = std::thread([this]()
    {
        try
        {
            auto bus = gst_pipeline_get_bus(GST_PIPELINE(this->pipeline));
            gst_bus_add_watch(bus, this->BusCallback, this);
            gst_object_unref(bus);

            if (gst_element_set_state(this->pipeline, GST_STATE_PLAYING) == GST_STATE_CHANGE_FAILURE)
            {
                log.Error("Failed to start pipeline!");
                return;
            }

            if (!this->streamLoop)
            {
                this->streamLoop = g_main_loop_new(NULL, FALSE);
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
