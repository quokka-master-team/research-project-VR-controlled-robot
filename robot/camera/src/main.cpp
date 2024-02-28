#include "ConfigReader.hpp"
#include "VideoStream.hpp"

int main(int argc, char *argv[])
{
    gst_init(nullptr, nullptr);
    ConfigReader configuration("config.yaml");
    VideoStream stream;

    try
    {
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

    gst_deinit();
    return 0;
}
