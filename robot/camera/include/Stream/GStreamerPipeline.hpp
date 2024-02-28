#pragma once
#include <gst/gst.h>
#include <string>

class GStreamerPipeline
{
public:
    GStreamerPipeline(const std::string& pipeline);
    ~GStreamerPipeline();

    std::string GetRaw() const;
    void ChangeToState(GstState state);

private:
    std::string pipelineText = "";
    GstElement* gstPipeline = nullptr;
};