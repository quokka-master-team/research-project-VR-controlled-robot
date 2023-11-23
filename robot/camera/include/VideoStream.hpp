#pragma once
#include <string>
#include <asio.hpp>

#include "GStreamerHandler.hpp"

class VideoStream
{
    GStreamerHandler& gstreamer = GStreamerHandler::Get();
    Log& log = Log::Get();

    std::unique_ptr<asio::ip::tcp::acceptor> acceptor;
    std::atomic<bool> listenToClient{false};
    std::thread listenerThread;
    asio::io_context clientContext;

    void HandleCommand(const std::string& command);
    void HandleRequest(std::shared_ptr<asio::ip::tcp::socket> socket);
    void ListenForRequests();

public:
    void ListenOn(const std::string& serverIp, unsigned short port);
    bool IsListening();

    ~VideoStream();
};