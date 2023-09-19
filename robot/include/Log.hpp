#include <spdlog/spdlog.h>

class Log
{
	Log() {
		spdlog::set_pattern("[%T] [%^%l%$] %v");
		spdlog::set_level(spdlog::level::info);
	}

	~Log() = default;

public:

	Log(const Log&) = delete;
	Log(Log&&) = delete;
	Log& operator=(Log) = delete;
	Log& operator=(Log&&) = delete;

	static Log& Get()
	{
		static Log instance;
		return instance;
	}

	void Info(const std::string& message) const
	{
		spdlog::info(message);
	}

	void Warning(const std::string& message) const
	{
		spdlog::warn(message);
	}

	void Error(const std::string& message) const
	{
		spdlog::error(message);
	}

	void Critical(const std::string& message) const
	{
		spdlog::critical(message);
	}
};