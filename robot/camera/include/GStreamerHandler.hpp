#pragma once
#include <gst/gst.h>
#include <gst/rtsp-server/rtsp-server.h>
#include <thread>
#include <string>

#include "Log.hpp"

class GStreamerHandler
{
    std::atomic<bool> isStreaming{false};
    std::thread streamingThread;

    std::string rawPipeline = "";
    GstElement* pipeline = nullptr;
    GMainLoop* streamLoop = nullptr;

    GstRTSPServer* rtspServer = nullptr;
    GstRTSPMediaFactory* mediaFactory = nullptr;

    Log& log = Log::Get();

    GStreamerHandler();
    ~GStreamerHandler();

    static gboolean BusCallback(GstBus *bus, GstMessage *msg, gpointer data);
    bool IsPipelineValid(GstElement* pipeline, GError *&handle);
    std::string ParsePipeline(const std::string &ipAddress, const std::string &port);
    void SetupStream();
    void Cleanup();

public:
    static GStreamerHandler& Get() {
        static GStreamerHandler instance;
        return instance;
    }

    GStreamerHandler(GStreamerHandler const&) = delete;
    void operator=(GStreamerHandler const&) = delete;

    void SetPipeline(const std::string& pipeline);
    void BuildPipeline(const std::string& ipAddress, const std::string& port, bool rtsp);
    void Start(bool rtsp);
    void Stop();
    bool IsStreaming();
};