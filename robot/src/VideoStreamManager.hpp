#include <gst/gst.h>

class VideoStreamManager {

    VideoStreamManager() {
        gst_init(nullptr, nullptr);
    }

    ~VideoStreamManager() {
        gst_deinit();
    }

public:
    static VideoStreamManager& GetInstance() {
        static VideoStreamManager instance;
        return instance;
    }

    VideoStreamManager(VideoStreamManager const&) = delete;
    void operator=(VideoStreamManager const&) = delete;
};