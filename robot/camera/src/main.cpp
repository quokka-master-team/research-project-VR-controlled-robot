#include "VideoStream.hpp"

int main(int argc, char *argv[])
{
    auto const streamName   = "Test stream";
    auto const serverIp     = "127.0.0.1";
    auto const serverPort   = 8080;

    auto pipeline = "v4l2src device=/dev/video0 ! videoconvert ! autovideosink";

    VideoStream stream(streamName);

    try 
    {
        stream.SetPipeline(pipeline);
        stream.ListenOn(serverIp, serverPort);

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
