#include "VideoStream.hpp"

int main(int argc, char *argv[])
{
    VideoStream stream("My video stream");
    stream.SetPipeline("v4l2src device=/dev/video0 ! videoconvert ! autovideosink");

    stream.Start();

    return 0;
}
