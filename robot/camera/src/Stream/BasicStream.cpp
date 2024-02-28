#include "Stream/BasicStream.hpp"

void BasicStream::Start()
{
    if (this->stream.joinable())
    {
        this->stream.join();
    }

    this->stream = std::thread([this]()
    {
        try
        {
            this->SetPipelineState(GST_STATE_PLAYING);
            g_main_loop_run(this->streamLoop);
            this->SetPipelineState(GST_STATE_READY);
        }
        catch (const std::exception& e)
        {
            log.Error(std::string(e.what()));
        }
    });
}
