cmake_minimum_required (VERSION 3.10)

project ("Camera")
file(GLOB src_files "include/*.hpp" "src/*.cpp")
add_executable (Camera ${src_files} )
include_directories(Camera PRIVATE "include")

set_property(TARGET Camera PROPERTY CXX_STANDARD 20)

# Find GStreamer package
find_package(PkgConfig REQUIRED)
pkg_search_module(gstreamer REQUIRED IMPORTED_TARGET gstreamer-1.0)
pkg_search_module(gstreamer-app REQUIRED IMPORTED_TARGET gstreamer-app-1.0)
pkg_search_module(gstreamer-video REQUIRED IMPORTED_TARGET gstreamer-video-1.0)

# Find GStreamer RTSP Server package
pkg_search_module(gstreamer-rtsp-server REQUIRED IMPORTED_TARGET gstreamer-rtsp-server-1.0)

# Find yaml-cpp package
find_package(yaml-cpp REQUIRED)
include_directories(${YAML_CPP_INCLUDE_DIRS})
target_link_libraries(Camera ${YAML_CPP_LIBRARIES})

# Find spdlog package
find_package(spdlog CONFIG REQUIRED)

# Find asio package
find_path(ASIO_INCLUDE_DIR 
    NAMES asio.hpp
    HINTS /usr/include
    PATH_SUFFIXES asio)
target_include_directories(Camera PRIVATE ${ASIO_INCLUDE_DIR})

# Link against libraries
target_link_libraries(Camera
    PkgConfig::gstreamer
    PkgConfig::gstreamer-app
    PkgConfig::gstreamer-video
    PkgConfig::gstreamer-rtsp-server
    spdlog::spdlog
    pthread
    rt
)
