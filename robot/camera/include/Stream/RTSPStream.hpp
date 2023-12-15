#pragma once
#include <asio.hpp>
#include <gst/rtsp-server/rtsp-server.h>

#include "Stream/GStreamer.hpp"

class RTSPStream : public GStreamer
{
public:
    virtual ~RTSPStream() override;

    void Start() override;
    void SetEndpoint(const std::string& ipAddress, const std::string& port);

private:
    bool IsEndpointAvaliable(const std::string& ipAddress, const std::string& port);
    void SetupEndpoint();
    void Cleanup();

    GstRTSPServer* rtspServer = nullptr;
    GstRTSPMediaFactory* mediaFactory = nullptr;

    std::string serverAddress = "127.0.0.1";
    std::string serverPort = "8554";
    const std::string serverPath = "/stream";

    Log& log = Log::Get();
};
