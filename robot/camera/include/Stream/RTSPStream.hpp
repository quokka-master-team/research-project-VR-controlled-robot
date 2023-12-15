#pragma once
#include <gst/rtsp-server/rtsp-server.h>

#include "Stream/GStreamer.hpp"

class RTSPStream : public GStreamer
{
public:
    virtual ~RTSPStream() override;

    void Start() override;
    void SetEndpoint(const std::string& ipAddress, const std::string& port);

private:
    void SetupEndpoint();
    void Cleanup();

    GstRTSPServer* rtspServer = nullptr;
    GstRTSPMediaFactory* mediaFactory = nullptr;

    std::string serverAddress;
    std::string serverPort;
    const std::string serverPath = "/stream";

    Log& log = Log::Get();
};
