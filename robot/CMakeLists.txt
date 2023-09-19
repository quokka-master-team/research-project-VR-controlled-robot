cmake_minimum_required (VERSION 3.13)

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
find_package(spdlog CONFIG REQUIRED)

# Link against GStreamer libraries
target_link_libraries(Robot
    PkgConfig::gstreamer
    PkgConfig::gstreamer-app
    PkgConfig::gstreamer-video
    spdlog::spdlog
)
