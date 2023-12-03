#include "VideoStream.hpp"
#include <stdexcept>
#include <chrono>

bool VideoStream::IsArgumentsCountValid(const std::vector<std::string> &arguments, int expected)
{
    if (arguments.size() != expected)
    {
        std::string argumentList = "";
        for (auto arg : arguments)
        {
            argumentList += arg + "; ";
        }

        log.Error("Expected " + std::to_string(expected) + " argument(s), got " + 
            std::to_string(arguments.size()) + ": " + argumentList);
        return false;
    }

    return true;
}

void VideoStream::HandleCommand(const std::string &command)
{
    auto commandText = std::istringstream(command);
    auto tokens = std::vector<std::string>
    {
        std::istream_iterator<std::string>
        {
            commandText
        },
        std::istream_iterator<std::string>{}
    };

    auto searchedCommand = this->command.find(tokens[0]);
    if (searchedCommand != this->command.end())
    {
        auto args = std::vector<std::string>(tokens.begin() + 1, tokens.end());
        
        if (log.IsDebugOn())
        {
            std::string restOfCommand;
            for (auto arg : args)
            {
                restOfCommand += " " + arg;
            }

            std::string remoteIP = listener.remote_endpoint().address().to_string();
            unsigned short remotePort = listener.remote_endpoint().port();

            log.Debug(remoteIP + ":" + std::to_string(remotePort) + " => " + searchedCommand->first + restOfCommand);
        }
        
        searchedCommand->second(args);
    }
    else
    {
        log.Warning("Received unknown command: " + command + ". Ignoring.");
    }
}

void VideoStream::HandleRequest()
{
    try
    {
        auto buffer = asio::streambuf();
        asio::read_until(listener, buffer, '\n');

        std::istream input(&buffer);
        std::string line;
        std::getline(input, line);

        if (!line.empty())
        {
            this->HandleCommand(line);
            listener.send(asio::buffer("Ok"));
        }
    }
    catch (const std::system_error& e)
    {
        auto reason = std::string(e.what());

        log.Warning("Bad character: " + reason);
        if (listener.is_open())
        {
            listener.send(asio::buffer("Fail: " + reason));
        }
        
        this->command["DISCONNECT"](std::vector<std::string>());
    }
}

void VideoStream::ListenForRequests()
{
    listener = acceptor->accept();

    this->closeSocketRequest = false;
    while (!this->closeSocketRequest)
    {
        this->HandleRequest();
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    if(listener.is_open())
    {
        listener.close();
    }
    log.Info("Client disconnected!");
}

VideoStream::VideoStream()
{
    this->command["START"] = [this](const std::vector<std::string>&)
    {
        if (this->ipAddress.empty())
        {
            log.Error("Cannot start streaming as ADDRESS wasn't specified!");
            return;
        }

        if (this->port.empty())
        {
            log.Error("Cannot start streaming as PORT wasn't specified!");
            return;
        }

        if (!gstreamer.IsStreaming())
        {
            log.Info("Starting stream...");
            gstreamer.BuildPipeline(this->ipAddress, this->port);
            gstreamer.Start();
        }
        else
        {
            log.Info("Stream is live already. Stop it to run again.");
        }
    };

    this->command["STOP"] = [this](const std::vector<std::string>& args)
    {
        if (gstreamer.IsStreaming())
        {
            log.Info("Stopping stream...");
            gstreamer.Stop();
        }
        else
        {
            log.Info("Stream wasn't live.");
        }
    };

    this->command["EXIT"] = [this](const std::vector<std::string>& args)
    {
        log.Info("Quitting...");

        this->command["DISCONNECT"](args);
        this->listenToClient.store(false);
    };

    this->command["SET"] = [this](const std::vector<std::string>& args)
    {
        if (!this->IsArgumentsCountValid(args, 2))
        {
            return;
        }

        if (args[0] == "ADDRESS")
        {
            this->ipAddress = args[1];
            log.Info("New IP address " + args[1] + " set!");
        }
        else if (args[0] == "PORT")
        {
            this->port = args[1];
            log.Info("New port " + args[1] + " set!");
        }
        else
        {
            log.Warning("Unknown parameter: " + args[0] + ". Aborting!");
        }
    };

    this->command["USE"] = [this](const std::vector<std::string>& args)
    {
        if (args.empty())
        {
            this->log.Error("Expected pipeline argument!");
            return;
        }

        std::string pipeline = "";
        for (auto arg : args)
        {
            pipeline += arg + " ";
        }

        if (gstreamer.IsStreaming())
        {
            gstreamer.Stop();
            gstreamer.SetPipeline(pipeline);
            gstreamer.Start();
        }
        else
        {
            gstreamer.SetPipeline(pipeline);
        }
    };

    this->command["DISCONNECT"] = [this](const std::vector<std::string>&)
    { 
        this->closeSocketRequest = true;
    };
}

void VideoStream::ListenOn(const std::string &serverIp, unsigned short port)
{
    log.Info("Binding to " + serverIp + ":" + std::to_string(port) + "...");

    acceptor = std::make_unique<asio::ip::tcp::acceptor>(
        this->context, asio::ip::tcp::endpoint(asio::ip::make_address(serverIp), port)
    );

    this->listenToClient.store(true);
    this->listenerThread = std::thread([this]() 
    {
        while (this->listenToClient.load())
        {
            this->ListenForRequests();
            std::this_thread::sleep_for(std::chrono::milliseconds(100));

            this->context.run();
            this->context.reset();
        }
    });
}

bool VideoStream::IsListening()
{
    return this->listenToClient.load();
}

VideoStream::~VideoStream()
{
    listenToClient.store(false);

    context.stop();

    if (listenerThread.joinable())
    {
        listenerThread.join();
    }

    log.Info("Stream closed!");
}
