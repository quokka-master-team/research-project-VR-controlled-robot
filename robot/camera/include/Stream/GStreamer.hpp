#pragma once
#include <thread>

#include "Stream/GStreamerPipeline.hpp"
#include "Log.hpp"

class GStreamer
{
public:
    GStreamer();
    virtual ~GStreamer();

    virtual void Start() = 0;
    bool IsStreaming();
    void Stop();

    void SetPipeline(const std::string &pipeline);
    std::string GetPipelineDescription() const;
    void SetPipelineState(GstState state);

protected:
    GMainLoop* streamLoop = nullptr;
    std::thread stream;

private:
    Log& log = Log::Get();
    std::unique_ptr<GStreamerPipeline> gstPipeline = nullptr;
};
