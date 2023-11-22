#pragma once
#include <string>
#include <asio.hpp>

#include "VideoStreamManager.hpp"

class VideoStream
{
    bool isStreaming = false;

    std::thread cameraThread;
    GstElement* pipeline = nullptr;
    GMainLoop* streamLoop = nullptr;

    std::thread streamingThread;
    std::atomic<bool> streamOverNetwork{false};

    std::unique_ptr<asio::ip::tcp::acceptor> acceptor;
    std::atomic<bool> listenToClient{false};
    std::thread listenerThread;
    asio::io_context clientContext;

    VideoStreamManager& manager = VideoStreamManager::Get();
    Log& log = Log::Get();

    void ValidatePipeline(GError*& handle);
    void PrepareStreamBuffer(
        asio::io_context& context,
        asio::posix::stream_descriptor& dataToStream,
        asio::ip::udp::socket& socket,
        asio::ip::udp::endpoint& endpoint
    );
    void HandleCommand(const std::string& command);
    void HandleRequest(std::shared_ptr<asio::ip::tcp::socket> socket);
    void ListenForRequests();

public:
    void SetPipeline(const std::string& str);
    void StreamOn(const std::string& serverIp, unsigned short port);
    void ListenOn(const std::string& serverIp, unsigned short port);
    bool IsListening();
    void Start();
    void Stop();

    ~VideoStream();
};