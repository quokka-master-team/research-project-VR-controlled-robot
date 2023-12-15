#pragma once
#include <functional>
#include <unordered_map>
#include <asio.hpp>

#include "Stream/BasicStream.hpp"
#include "Stream/RTSPStream.hpp"

class VideoStream
{
public:
    VideoStream();
    ~VideoStream();

    void ListenOn(const std::string& serverIp, unsigned short port);
    bool IsListening();

private:
    Log& log = Log::Get();
    std::unique_ptr<GStreamer> stream = nullptr;

    std::unordered_map<
        std::string, 
        std::function<void(const std::vector<std::string>&)>
    > command;

    asio::io_context context;
    asio::ip::tcp::socket listener = asio::ip::tcp::socket(context);
    std::unique_ptr<asio::ip::tcp::acceptor> acceptor;

    std::atomic<bool> listenToClient{false};
    std::thread listenerThread;

    bool closeSocketRequest = false;

    bool IsArgumentsCountValid(const std::vector<std::string>& arguments, int expected);
    void HandleCommand(const std::string& command);
    void HandleRequest();

    void ListenForRequests();
};