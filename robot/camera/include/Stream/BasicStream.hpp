#pragma once
#include <thread>

#include "Stream/GStreamer.hpp"

class BasicStream : public GStreamer
{
public:
    void Start() override;

private:
    Log& log = Log::Get();
};
