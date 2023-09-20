#include "VideoStream.hpp"
#include <stdexcept>
#include <chrono>

void VideoStream::ValidatePipeline(GError*& handle)
{
    if (handle)
    {
        throw std::runtime_error("Failed to create pipeline: " + std::string(handle->message));
    }

    if (!this->pipeline)
    {
        throw std::runtime_error("Failed to create pipeline: Unknown error.");
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

            log.Info("Received command: " + line);

            if (line == "START")    this->Start();
            if (line == "STOP")     this->Stop();
            if (line == "EXIT")     this->listenToClient.store(false);
            
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

void VideoStream::SetPipeline(const std::string& str)
{
    if (this->pipeline != nullptr)
    {
        gst_object_unref(GST_OBJECT(this->pipeline));
    }

    GError* errorHandle = nullptr;
    this->pipeline = gst_parse_launch(str.c_str(), &errorHandle);

    this->ValidatePipeline(errorHandle);
}

void VideoStream::ListenOn(const std::string &serverIp, unsigned short port)
{
    acceptor = std::make_unique<asio::ip::tcp::acceptor>(
        this->clientContext, asio::ip::tcp::endpoint(asio::ip::make_address(serverIp), port)
    );

    this->listenToClient.store(true);
    this->clientListener = std::thread([this]() 
    {
        while (this->listenToClient.load())
        {
            this->ListenForRequests();
            std::this_thread::sleep_for(std::chrono::milliseconds(100));

            this->clientContext.run();
            this->clientContext.reset();
        }
    });

    log.Info(name + " is listening on " + serverIp + ":" + std::to_string(port));
}

bool VideoStream::IsListening()
{
    return this->listenToClient.load();
}

void VideoStream::Start()
{
    if (gst_element_set_state(pipeline, GST_STATE_PLAYING) == GST_STATE_CHANGE_FAILURE)
    {
        throw std::runtime_error("Failed to start pipeline!");
    }

    this->streamLoop = g_main_loop_new(NULL, FALSE);
    this->streamThread = std::make_unique<std::thread>([this]() {
        g_main_loop_run(this->streamLoop);
    });
}

void VideoStream::Stop()
{
    if (this->streamLoop)
    {
        g_main_loop_quit(this->streamLoop);
        gst_element_set_state(this->pipeline, GST_STATE_NULL);
    }

    if (this->streamThread && this->streamThread->joinable()) {
        this->streamThread->join();
    }
}

VideoStream::~VideoStream()
{
    this->listenToClient.store(false);
    this->clientContext.stop();

    if (this->clientListener.joinable())
    {
        this->clientListener.join();
    }

    this->Stop();

    if (this->pipeline)
    {
        gst_element_set_state(pipeline, GST_STATE_NULL);
        gst_object_unref(GST_OBJECT(this->pipeline));
    }

    if (this->streamLoop)
    {
        g_main_loop_unref(this->streamLoop);
    }
    
    log.Info(this->name + " closed!");
}
