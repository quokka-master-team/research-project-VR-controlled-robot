#include <string>
#include "VideoStreamManager.hpp"

class VideoStream
{
    std::string name;
    GstElement* pipeline = nullptr;
    GMainLoop* streamLoop = nullptr;
    VideoStreamManager& manager = VideoStreamManager::GetInstance();

    void ValidatePipeline(GError*& handle);

public:
    VideoStream(const std::string&  name = "undefined") : name(name)
    {}

    void SetPipeline(const std::string& str);
    void Start();
    void Stop();

    ~VideoStream();
};