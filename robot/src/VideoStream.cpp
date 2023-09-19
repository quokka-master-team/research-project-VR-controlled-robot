#include "VideoStream.hpp"
#include <stdexcept>

void VideoStream::ValidatePipeline(GError*& handle)
{
    if (!this->pipeline)
    {
        if (handle)
        {
            throw std::runtime_error("Failed to create pipeline: " + std::string(handle->message));
        }
        
        throw std::runtime_error("Failed to create pipeline: Unknown error!");
    }
}

void VideoStream::SetPipeline(const std::string& str)
{
    if (this->pipeline != nullptr)
    {
        gst_object_unref(GST_OBJECT(this->pipeline));
    }

    GError* errorHandle = nullptr;
    this->pipeline = gst_parse_launch(str.c_str(), &errorHandle);

    this->ValidatePipeline(errorHandle);
}

void VideoStream::Start()
{
    if (gst_element_set_state(pipeline, GST_STATE_PLAYING) == GST_STATE_CHANGE_FAILURE)
    {
        throw std::runtime_error("Failed to start pipeline!");
    }

    this->streamLoop = g_main_loop_new(NULL, FALSE);
    g_main_loop_run(this->streamLoop);
}

VideoStream::~VideoStream()
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
}
