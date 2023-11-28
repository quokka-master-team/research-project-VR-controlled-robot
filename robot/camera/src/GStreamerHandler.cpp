#include "GStreamerHandler.hpp"

GStreamerHandler::GStreamerHandler()
{
    gst_init(nullptr, nullptr);
    log.Info("Streaming initialized successfully!");
}

GStreamerHandler::~GStreamerHandler()
{
    this->Stop();

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

            handler->Stop();
            break;

        case GST_MESSAGE_EOS:
            handler->log.Info("GStreamer: End of stream");
            
            handler->Stop();
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

    if (this->isStreaming)
    {
        log.Warning("Stream is already live!");
        return;
    }

    auto bus = gst_pipeline_get_bus(GST_PIPELINE(this->pipeline));
    gst_bus_add_watch(bus, this->BusCallback, this);
    gst_object_unref(bus);

    if (gst_element_set_state(this->pipeline, GST_STATE_PLAYING) == GST_STATE_CHANGE_FAILURE)
    {
        log.Error("Failed to start pipeline!");
        return;
    }

    this->streamLoop = g_main_loop_new(NULL, FALSE);
    this->streamingThread = std::thread([this]()
    {
        g_main_loop_run(this->streamLoop);
    });

    this->isStreaming = true;
}

void GStreamerHandler::Stop()
{
    if (!this->isStreaming)
    {
        return;
    }

    if (this->streamLoop)
    {
        gst_element_set_state(this->pipeline, GST_STATE_NULL);
        g_main_loop_quit(this->streamLoop);
    }

    if (streamingThread.joinable())
    {
        streamingThread.join();
    }
    this->isStreaming = false;
}

bool GStreamerHandler::IsStreaming()
{
    return isStreaming.load();
}
