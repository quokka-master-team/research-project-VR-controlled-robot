#include "Stream/GStreamerPipeline.hpp"
#include <stdexcept>

GStreamerPipeline::GStreamerPipeline(const std::string &pipeline) : gstPipeline(nullptr), pipelineText(pipeline)
{
    GError* error = nullptr;
    this->gstPipeline = gst_parse_launch(pipeline.c_str(), &error);

    if (!this->gstPipeline || error)
    {
        auto message = error ? std::string(error->message) : "Unknown error";
        if (error)
        {
            g_clear_error(&error);
        }

        if (this->gstPipeline)
        {
            gst_object_unref(this->gstPipeline);
            this->gstPipeline = nullptr;
        }

        throw std::runtime_error("Pipeline initialization failed: " + message);
    }

    this->ChangeToState(GST_STATE_READY);
}

GStreamerPipeline::~GStreamerPipeline()
{
    if (this->gstPipeline)
    {
        gst_element_set_state(this->gstPipeline, GST_STATE_NULL);
        gst_object_unref(this->gstPipeline);
        this->gstPipeline = nullptr;
    }
}

std::string GStreamerPipeline::GetRaw() const
{
    return this->pipelineText;
}

void GStreamerPipeline::ChangeToState(GstState state)
{
    if (gst_element_set_state(this->gstPipeline, state) == GST_STATE_CHANGE_FAILURE)
    {
        switch (state)
        {
            case GST_STATE_PLAYING:
            case GST_STATE_READY:
                throw std::runtime_error("Pipeline won't start! Maybe third-party issues?");

            case GST_STATE_NULL:
                throw std::runtime_error("Cannot terminate the pipeline! Something is blocking it?");

            default:
                throw std::invalid_argument("Oh! Hmm.. no, never heard of the guy. (I'm not handling this state)");
        }
    } 
}
