#pragma once
#include <string>
#include <functional>
#include <unordered_map>
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

    std::unordered_map<std::string, std::function<void(const std::vector<std::string>&)>> command;

    std::string ipAddress;
    std::string port;

    bool IsArgumentsCountValid(const std::vector<std::string>& arguments, int expected);
    void HandleCommand(const std::string& command);
    void HandleRequest(std::shared_ptr<asio::ip::tcp::socket> socket);
    void ListenForRequests();

public:
    VideoStream();

    void ListenOn(const std::string& serverIp, unsigned short port);
    bool IsListening();

    ~VideoStream();
};