#include "VideoStream.hpp"
#include <stdexcept>
#include <chrono>
#include <gst/app/gstappsink.h>

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

void VideoStream::PrepareStreamBuffer(
    asio::io_context& context, 
    asio::posix::stream_descriptor& dataToStream,
    asio::ip::udp::socket& socket,
    asio::ip::udp::endpoint& endpoint)
{
    
}

void VideoStream::HandleCommand(const std::string& command)
{
    log.Info("Received command: " + command);

    if (command == "START")    this->Start();
    if (command == "STOP")     this->Stop();
    if (command == "EXIT")
    {
        if (isStreaming)
        {
            this->Stop();
        }

        this->listenToClient.store(false);
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

void VideoStream::StreamOn(const std::string &serverIp, unsigned short port)
{
    log.Info("Binding to " + serverIp + ":" + std::to_string(port) + "...");

    Start();

    this->streamOverNetwork.store(true);
    this->streamingThread = std::thread([this, /*streamPipe,*/ serverIp, port]() 
    {
        log.Info("Going live!");

        asio::io_context context;
        auto socket = asio::ip::udp::socket(context, asio::ip::udp::v4());
        auto endpoint = asio::ip::udp::endpoint(asio::ip::make_address(serverIp), asio::ip::port_type(port));

        auto appsink = GST_APP_SINK(gst_bin_get_by_name(GST_BIN(pipeline), "stream"));
        

        while (this->streamOverNetwork.load())
        {
            GstSample* sample = gst_app_sink_pull_sample(appsink);

            if (sample)
            {
                GstBuffer* buffer = gst_sample_get_buffer(sample);
                GstMapInfo map;

                if (gst_buffer_map(buffer, &map, GST_MAP_READ))
                {
                    try
                    {
                        // Send the buffer data over UDP using ASIO
                        socket.send_to(asio::buffer(map.data, map.size), endpoint);
                    }
                    catch (const std::system_error& e)
                    {
                        printf("Message size: %ld\n", map.size);
                        log.Critical(e.what());
                    }

                    gst_buffer_unmap(buffer, &map);
                }

                gst_sample_unref(sample);
            }
        }
    });
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

void VideoStream::Start()
{
    if (isStreaming)
    {
        this->log.Warning("Stream is already live!");
        return;
    }

    if (gst_element_set_state(pipeline, GST_STATE_PLAYING) == GST_STATE_CHANGE_FAILURE)
    {
        throw std::runtime_error("Failed to start pipeline!");
    }

    this->streamLoop = g_main_loop_new(NULL, FALSE);
    this->cameraThread = std::thread([this]()
    {
        g_main_loop_run(this->streamLoop);
    });
    this->isStreaming = true;
}

void VideoStream::Stop()
{
    if (!this->isStreaming)
    {
        return;
    }

    // 1. Stop sending stream over network
    if (this->streamOverNetwork.load())
    {
        this->streamOverNetwork.store(false);
        if (this->streamingThread.joinable())
        {
            this->streamingThread.join();
        }
    }
    
    // 2. Stop the recording process
    if (this->streamLoop)
    {
        gst_element_set_state(this->pipeline, GST_STATE_NULL);
        g_main_loop_quit(this->streamLoop);
    }

    if (this->cameraThread.joinable())
    {
        this->cameraThread.join();
    }
    this->isStreaming = false;
}

VideoStream::~VideoStream()
{
    Stop();
    this->clientContext.stop();

    if (this->listenerThread.joinable())
    {
        this->listenerThread.join();
    }

    if (this->pipeline)
    {
        gst_element_set_state(pipeline, GST_STATE_NULL);
        gst_object_unref(GST_OBJECT(this->pipeline));
    }

    if (this->streamLoop)
    {
        g_main_loop_unref(this->streamLoop);
    }
    
    log.Info("Stream closed!");
}
