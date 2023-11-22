#include "ConfigReader.hpp"
#include "VideoStream.hpp"

int main(int argc, char *argv[])
{
    ConfigReader configuration("config.yaml");
    VideoStream stream;

    auto pipeline = "v4l2src ! videoconvert ! jpegenc quality=50 ! appsink name=stream";

    try 
    {
        stream.SetPipeline(pipeline);
        stream.StreamOn(configuration.getStreamingServerIp(), configuration.getStreamingPort());
        stream.ListenOn(configuration.getManagementServerIp(), configuration.getManagementPort());

        while (stream.IsListening()) 
        {
            // Prevents throttling over the network and wasting CPU recources
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        }
    }
    catch (const std::exception& e)
    {
        Log::Get().Critical(e.what());
    }

    return 0;
}
