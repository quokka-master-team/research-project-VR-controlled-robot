#include <unistd.h>
#include "VideoStream.hpp"

int main(int argc, char *argv[])
{
    auto streamName   = "Test stream";
    auto serverIp     = "127.0.0.1";
    auto serverPort   = 8080;

    auto pipeline = "v4l2src device=/dev/video0 ! videoconvert ! autovideosink";

    int opt;
    while ((opt = getopt(argc, argv, "s:p:l:")) != -1)
    {
        switch (opt)
        {
            case 's':
                serverIp = optarg;
                break;
            case 'p':
                serverPort = std::stoi(optarg);
                break;
            case 'P':
                pipeline = optarg;
                break;
            default:
                printf("All possible options:\n");
                printf("-P <gstreamer_pipeline>: Pipeline settings for camera configuration.\n");
                printf("-s <server_ip>: IP of the server that requests commands.\n");
                printf("-p <port>: Port of the server from which requests are sent.\n");
                return 1;
        }
    }

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
