#include "VideoStream.hpp"
#include <stdexcept>
#include <chrono>
#include <gst/app/gstappsink.h>

void VideoStream::HandleCommand(const std::string& command)
{
    auto result = this->command.find(command);

    if (result != this->command.end())
    {
        result->second();
    }
    else
    {
        log.Warning("Received unknown command: " + command + ". Ignoring.");
    }
}

void VideoStream::HandleRequest(std::shared_ptr<asio::ip::tcp::socket> socket)
{
    auto buffer = std::make_shared<asio::streambuf>();
    asio::async_read_until(*socket, *buffer, "\n", 
        [this, buffer, socket](const asio::error_code& error, size_t)
        {
            if (error)
            {
                log.Error("Error while retreiving client message: " + error.message());
                socket->close();

                return;
            }

            std::istream input(buffer.get());
            std::string line;
            std::getline(input, line);

            this->HandleCommand(line);
            
            socket->close();
        }
    );
}

void VideoStream::ListenForRequests()
{
    acceptor->async_accept(
        [this](const asio::error_code& error, asio::ip::tcp::socket socket) 
        {
            if (error)
            {
                log.Error("Error while setting up endpoint: " + error.message());
                return;
            }

            this->HandleRequest(
                std::make_shared<asio::ip::tcp::socket>(std::move(socket))
            );
        }
    );
}

VideoStream::VideoStream()
{
    command["START"] = [this]()
    {
        if (!gstreamer.IsStreaming())
        {
            gstreamer.Start();
        }
    };

    command["STOP"] = [this]()
    {
        if (gstreamer.IsStreaming())
        {
            gstreamer.Stop();
        }
    };

    command["EXIT"] = [this]()
    {
        listenToClient.store(false);
    };
}

void VideoStream::ListenOn(const std::string &serverIp, unsigned short port)
{
    log.Info("Binding to " + serverIp + ":" + std::to_string(port) + "...");

    acceptor = std::make_unique<asio::ip::tcp::acceptor>(
        this->clientContext, asio::ip::tcp::endpoint(asio::ip::make_address(serverIp), port)
    );

    this->listenToClient.store(true);
    this->listenerThread = std::thread([this]() 
    {
        while (this->listenToClient.load())
        {
            this->ListenForRequests();
            std::this_thread::sleep_for(std::chrono::milliseconds(100));

            this->clientContext.run();
            this->clientContext.reset();
        }
    });
}

bool VideoStream::IsListening()
{
    return this->listenToClient.load();
}

VideoStream::~VideoStream()
{
    command["STOP"]();

    clientContext.stop();

    if (listenerThread.joinable())
    {
        listenerThread.join();
    }

    log.Info("Stream closed!");
}
