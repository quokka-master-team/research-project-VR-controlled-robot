#pragma once
#include <string>
#include <yaml-cpp/yaml.h>

class ConfigReader
{
    std::string managementServerIp;
    unsigned short managementPort;

    std::string streamingServerIp;
    unsigned short streamingPort;

public:
    ConfigReader(const std::string& filename)
    {
        auto config = YAML::LoadFile(filename);

        managementServerIp = config["management"]["server"].as<std::string>();
        managementPort = config["management"]["port"].as<unsigned short>();
        
        streamingServerIp = config["streaming"]["server"].as<std::string>();
        streamingPort = config["streaming"]["port"].as<unsigned short>();
    }

    std::string getManagementServerIp()
    {
        return managementServerIp;
    }

    unsigned short getManagementPort()
    {
        return managementPort;
    }

    std::string getStreamingServerIp()
    {
        return streamingServerIp;
    }

    unsigned short getStreamingPort()
    {
        return streamingPort;
    }
};