#include "VideoStream.hpp"

int main(int argc, char *argv[])
{
    VideoStream stream("My video stream");

    try 
    {
        stream.SetPipeline("v4l2src device=/dev/video0 ! videoconvert ! autovideosink");
        stream.Start();
    }
    catch (const std::exception& e)
    {
        Log::Get().Critical(e.what());
    }

    return 0;
}
