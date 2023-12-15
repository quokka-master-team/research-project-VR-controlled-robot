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
    this->serverAddress = ipAddress;
    this->serverPort = port;

    log.Info("RTSP will be hosted on rtsp://" + ipAddress + ":" + port + this->serverPath);
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
