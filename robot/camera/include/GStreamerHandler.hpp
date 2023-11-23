#pragma once
#include <gst/gst.h>
#include <thread>
#include <string>

#include "Log.hpp"

class GStreamerHandler
{
    std::atomic<bool> isStreaming{false};
    std::thread streamingThread;

    GstElement* pipeline = nullptr;
    GMainLoop* streamLoop = nullptr;

    Log& log = Log::Get();

    GStreamerHandler();
    ~GStreamerHandler();

    void ValidatePipeline(GError*& handle);

public:
    static GStreamerHandler& Get() {
        static GStreamerHandler instance;
        return instance;
    }

    GStreamerHandler(GStreamerHandler const&) = delete;
    void operator=(GStreamerHandler const&) = delete;

    void SetPipeline(const std::string& pipeline);
    void Start();
    void Stop();
    bool IsStreaming();
};