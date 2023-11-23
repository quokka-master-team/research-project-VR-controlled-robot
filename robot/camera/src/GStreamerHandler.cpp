#include "GStreamerHandler.hpp"

GStreamerHandler::GStreamerHandler()
{
    gst_init(nullptr, nullptr);
    log.Info("Streaming initialized successfully!");
}

GStreamerHandler::~GStreamerHandler()
{
    if (this->pipeline)
    {
        gst_element_set_state(pipeline, GST_STATE_NULL);
        gst_object_unref(GST_OBJECT(this->pipeline));
    }

    if (this->streamLoop)
    {
        g_main_loop_unref(this->streamLoop);
    }

    gst_deinit();
    log.Info("Goodbye! (~˘▾˘)~");
}

void GStreamerHandler::ValidatePipeline(GError *&handle)
{
    if (handle)
    {
        throw std::runtime_error("Failed to create pipeline: " + std::string(handle->message));
    }

    if (!this->pipeline)
    {
        throw std::runtime_error("Failed to create pipeline: Unknown error.");
    }
}

void GStreamerHandler::SetPipeline(const std::string &pipeline)
{
    if (this->pipeline != nullptr)
    {
        gst_object_unref(GST_OBJECT(this->pipeline));
    }

    GError* errorHandle = nullptr;
    this->pipeline = gst_parse_launch(pipeline.c_str(), &errorHandle);

    this->ValidatePipeline(errorHandle);
}

void GStreamerHandler::Start()
{
    if (isStreaming)
    {
        log.Warning("Stream is already live!");
        return;
    }

    if (gst_element_set_state(pipeline, GST_STATE_PLAYING) == GST_STATE_CHANGE_FAILURE)
    {
        throw std::runtime_error("Failed to start pipeline!");
    }

    streamLoop = g_main_loop_new(NULL, FALSE);
    streamingThread = std::thread([this]()
    {
        g_main_loop_run(this->streamLoop);
    });
    isStreaming = true;
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
