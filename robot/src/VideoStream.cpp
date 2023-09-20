#include "VideoStream.hpp"
#include <stdexcept>

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

void VideoStream::HandleClient(asio::ip::tcp::socket socket)
{
    auto buffer = std::make_shared<asio::streambuf>();
    asio::async_read_until(socket, *buffer, "\n", 
        [this, buffer, &socket](const asio::error_code& error, size_t)
        {
            if (error)
            {
                log.Error("Error while retreiving client message: " + error.message());
                socket.close();

                return;
            }

            std::istream input(buffer.get());
            std::string line;
            std::getline(input, line);

            if (line == "START")    this->Start();
            if (line == "STOP")     this->Stop();
            
            socket.close();
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

    acceptor->async_accept(
        [this, ip=serverIp, port=port](const asio::error_code& error, asio::ip::tcp::socket socket) 
        {
            if (error)
            {
                log.Error("Error while setting up endpoint: " + error.message());
                return;
            }

            this->HandleClient(std::move(socket));
            this->ListenOn(ip, port);
        }
    );

    this->clientListener = std::thread([this]() 
    {
        while (!this->exitThread.load()) {
            this->clientContext.run();
            this->clientContext.reset();
        }
    });

    log.Info(name + " is listening on " + serverIp + ":" + std::to_string(port));
}

void VideoStream::Start()
{
    if (gst_element_set_state(pipeline, GST_STATE_PLAYING) == GST_STATE_CHANGE_FAILURE)
    {
        throw std::runtime_error("Failed to start pipeline!");
    }

    this->streamLoop = g_main_loop_new(NULL, FALSE);
    g_main_loop_run(this->streamLoop);
}

void VideoStream::Stop()
{
    if (this->streamLoop)
    {
        g_main_loop_quit(this->streamLoop);
        gst_element_set_state(this->pipeline, GST_STATE_NULL);
    }
}

VideoStream::~VideoStream()
{
    if (this->pipeline)
    {
        gst_element_set_state(pipeline, GST_STATE_NULL);
        gst_object_unref(GST_OBJECT(this->pipeline));
        log.Info("Pipeline closed!");
    }

    if (this->streamLoop)
    {
        g_main_loop_unref(this->streamLoop);
        log.Info("Stream closed!");
    }

    this->exitThread.store(true);
    this->clientContext.stop();

    if (this->clientListener.joinable()) {
        this->clientListener.join();
    }
    log.Info("Stopped client listener!");
}
