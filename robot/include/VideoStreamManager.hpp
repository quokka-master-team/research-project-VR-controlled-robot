#include "Log.hpp"
#include <gst/gst.h>

class VideoStreamManager {

    Log& log = Log::Get();

    VideoStreamManager() {
        gst_init(nullptr, nullptr);
        log.Info("Streaming initialized successfully!");
    }

    ~VideoStreamManager() {
        gst_deinit();
        log.Info("Goodbye! (~˘▾˘)~");
    }

public:
    static VideoStreamManager& Get() {
        static VideoStreamManager instance;
        return instance;
    }

    VideoStreamManager(VideoStreamManager const&) = delete;
    void operator=(VideoStreamManager const&) = delete;
};