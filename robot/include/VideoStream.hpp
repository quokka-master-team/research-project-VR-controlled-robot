#include <string>
#include <asio.hpp>

#include "VideoStreamManager.hpp"

class VideoStream
{
    std::string name;

    std::unique_ptr<std::thread> streamThread;
    GstElement* pipeline = nullptr;
    GMainLoop* streamLoop = nullptr;

    std::unique_ptr<asio::ip::tcp::acceptor> acceptor;
    std::atomic<bool> listenToClient{false};
    std::thread clientListener;
    asio::io_context clientContext;

    VideoStreamManager& manager = VideoStreamManager::Get();
    Log& log = Log::Get();

    void ValidatePipeline(GError*& handle);
    void HandleRequest(std::shared_ptr<asio::ip::tcp::socket> socket);
    void ListenForRequests();

public:
    VideoStream(const std::string& name) : name(name)
    {}

    void SetPipeline(const std::string& str);
    void ListenOn(const std::string& serverIp, unsigned short port);
    bool IsListening();
    void Start();
    void Stop();

    ~VideoStream();
};