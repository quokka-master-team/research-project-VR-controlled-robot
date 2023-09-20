#include <string>
#include <asio.hpp>

#include "VideoStreamManager.hpp"

class VideoStream
{
    std::string name;
    GstElement* pipeline = nullptr;
    GMainLoop* streamLoop = nullptr;

    std::unique_ptr<asio::ip::tcp::acceptor> acceptor;
    std::atomic<bool> exitThread{false};
    std::thread clientListener;
    asio::io_context clientContext;

    VideoStreamManager& manager = VideoStreamManager::Get();
    Log& log = Log::Get();

    void ValidatePipeline(GError*& handle);
    void HandleClient(asio::ip::tcp::socket socket);
    

public:
    VideoStream(const std::string& name = "undefined") : name(name)
    {}

    void SetPipeline(const std::string& str);
    void ListenOn(const std::string& serverIp, unsigned short port);
    void Start();
    void Stop();

    ~VideoStream();
};