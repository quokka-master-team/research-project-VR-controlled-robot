#include "Stream/RTSPStream.hpp"

RTSPStream::~RTSPStream()
{
    Cleanup();
}

void RTSPStream::Start()
{
    try
    {
        // RTSP library requires server reinitialization for reuse
        this->Cleanup();
        this->SetupEndpoint();

        gst_rtsp_media_factory_set_launch(this->mediaFactory, this->GetPipelineDescription().c_str());
        gst_rtsp_media_factory_set_shared(this->mediaFactory, TRUE);

        gst_rtsp_server_attach(this->rtspServer, NULL);

        this->stream = std::thread([this]()
        {
            g_main_loop_run(this->streamLoop);
        });
    }
    catch(const std::exception& e)
    {
        log.Error(e.what());
        return;
    }
}

void RTSPStream::SetEndpoint(const std::string &ipAddress, const std::string &port)
{
    try
    {
        if (!IsEndpointAvaliable(ipAddress, port))
        {
            log.Warning("The address is already occupied. You might have issues with connecting to the server...");
        }

        this->serverAddress = ipAddress;
        this->serverPort = port;
    }
    catch(const std::exception& e)
    {
        log.Error(e.what());
        log.Warning("The default settings were loaded.");
    }

    log.Info("RTSP will be hosted on rtsp://" + this->serverAddress + ":" + this->serverPort + this->serverPath);
}

bool RTSPStream::IsEndpointAvaliable(const std::string& ipAddress, const std::string& port)
{
    int portToCheck;

    try {
        portToCheck = std::stoi(port);

        if (portToCheck < 0 || portToCheck > 65535)
        {
            throw std::out_of_range("Port number out of range");
        }
    }
    catch (const std::invalid_argument& e)
    {
        throw std::runtime_error("Invalid port number!");
        return false;
    }
    catch (const std::out_of_range& e)
    {
        throw std::runtime_error("Port number out of range!");
        return false;
    }

    asio::io_context io_context;
    asio::ip::tcp::endpoint endpoint(asio::ip::make_address(ipAddress), asio::ip::port_type(portToCheck));
    asio::ip::tcp::socket socket(io_context);

    asio::error_code ec;
    socket.open(endpoint.protocol(), ec);
    if (ec) 
    {
        return false;
    }

    socket.bind(endpoint, ec);
    if (ec) 
    {
        return false;
    }

    return true;
}

void RTSPStream::SetupEndpoint()
{
    this->rtspServer = gst_rtsp_server_new();
    this->mediaFactory = gst_rtsp_media_factory_new();

    gst_rtsp_server_set_address(this->rtspServer, this->serverAddress.c_str());
    gst_rtsp_server_set_service(this->rtspServer, this->serverPort.c_str());

    auto mountPoint = gst_rtsp_server_get_mount_points(this->rtspServer);
    gst_rtsp_mount_points_add_factory(mountPoint, this->serverPath.c_str(), this->mediaFactory);
    gst_object_unref(mountPoint);
}

void RTSPStream::Cleanup()
{
    if (this->mediaFactory && GST_IS_OBJECT(this->mediaFactory))
    {
        gst_object_unref(this->mediaFactory);
        this->mediaFactory = nullptr;
    }

    if (this->rtspServer && GST_IS_OBJECT(this->rtspServer))
    {
        gst_object_unref(this->rtspServer);
        this->rtspServer = nullptr;
    }
}
