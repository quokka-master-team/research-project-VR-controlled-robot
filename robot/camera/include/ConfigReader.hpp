#pragma once
#include <string>
#include <yaml-cpp/yaml.h>

class ConfigReader
{
    YAML::Node config;

public:
    ConfigReader(const std::string& filename)
    {
        config = YAML::LoadFile(filename);
    }

    std::string getManagementServerIp()
    {
        return config["management"]["server"].as<std::string>();
    }

    unsigned short getManagementPort()
    {
        return config["management"]["port"].as<unsigned short>();
    }

    std::string getStreamingServerIp()
    {
        return config["streaming"]["server"].as<std::string>();
    }

    unsigned short getStreamingPort()
    {
        return config["streaming"]["port"].as<unsigned short>();
    }

    std::string getPipeline(const std::string& name)
    {
        return config[name].as<std::string>();
    }
};