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
    asio::io_context context;

    std::unordered_map<
        std::string, 
        std::function<void(const std::vector<std::string>&)>
    > command;

    std::string ipAddress;
    std::string port;
    asio::ip::tcp::socket listener = asio::ip::tcp::socket(context);
    bool closeSocketRequest = false;

    bool IsArgumentsCountValid(const std::vector<std::string>& arguments, int expected);
    void HandleCommand(const std::string& command);
    void HandleRequest();
    void ListenForRequests();

public:
    VideoStream();

    void ListenOn(const std::string& serverIp, unsigned short port);
    bool IsListening();

    ~VideoStream();
};