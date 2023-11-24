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

bool GStreamerHandler::IsPipelineValid(GstElement* pipeline, GError *&handle)
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

    if (gst_element_set_state(this->pipeline, GST_STATE_PLAYING) == GST_STATE_CHANGE_FAILURE)
    {
        throw std::runtime_error("Failed to start pipeline!");
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
