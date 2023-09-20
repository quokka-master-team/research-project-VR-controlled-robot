cmake_minimum_required (VERSION 3.10)

project ("Robot")
file(GLOB src_files "include/*.hpp" "src/*.cpp")
add_executable (Robot ${src_files} )
include_directories(Robot PRIVATE "include")

set_property(TARGET Robot PROPERTY CXX_STANDARD 20)

# Find GStreamer package
find_package(PkgConfig REQUIRED)
pkg_search_module(gstreamer REQUIRED IMPORTED_TARGET gstreamer-1.0)
pkg_search_module(gstreamer-app REQUIRED IMPORTED_TARGET gstreamer-app-1.0)
pkg_search_module(gstreamer-video REQUIRED IMPORTED_TARGET gstreamer-video-1.0)

# Find spdlog package
find_package(spdlog CONFIG REQUIRED)

# Find asio package
find_path(ASIO_INCLUDE_DIR 
    NAMES asio.hpp
    HINTS /usr/include
    PATH_SUFFIXES asio)
target_include_directories(Robot PRIVATE ${ASIO_INCLUDE_DIR})

# Link against libraries
target_link_libraries(Robot
    PkgConfig::gstreamer
    PkgConfig::gstreamer-app
    PkgConfig::gstreamer-video
    spdlog::spdlog
    pthread
    rt
)
