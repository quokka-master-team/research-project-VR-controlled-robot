#include "Stream/GStreamer.hpp"

GStreamer::GStreamer()
{
    this->streamLoop = g_main_loop_new(NULL, FALSE);
}

GStreamer::~GStreamer()
{
    if (this->streamLoop)
    {
        if (this->IsStreaming())
        {
            this->Stop();
        }
        
        g_main_loop_unref(this->streamLoop);
    }
    
    this->streamLoop = nullptr;
}

bool GStreamer::IsStreaming()
{
    return g_main_loop_is_running(this->streamLoop);
}

void GStreamer::Stop()
{
    g_main_loop_quit(this->streamLoop);

    if (this->stream.joinable())
    {
        this->stream.join();
    }
}

void GStreamer::SetPipeline(const std::string &pipeline)
{
    try 
    {
        this->gstPipeline = std::make_unique<GStreamerPipeline>(pipeline);
    }
    catch(const std::exception& e)
    {
        log.Error(e.what());
        this->gstPipeline = nullptr;
    }
}

std::string GStreamer::GetPipelineDescription() const
{
    if (this->gstPipeline == nullptr)
    {
        throw std::runtime_error("Pipeline is undefined or didn't pass validation check.");
    }

    return this->gstPipeline->GetRaw();
}

void GStreamer::SetPipelineState(GstState state)
{
    if (this->gstPipeline == nullptr)
    {
        throw std::runtime_error("Pipeline is not defined! So you want to change the state of what?");
    }

    this->gstPipeline->ChangeToState(state);
}
