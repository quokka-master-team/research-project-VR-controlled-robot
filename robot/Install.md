# Tutorial
Dedicated **only** for Linux 🐧

## Installation [Debian]
1. Update packages
    ```bash
    sudo apt-get update
    sudo apt-get upgrade
    ```
2. Install basic prerequisites
    ```bash
    sudo apt-get install build-essential cmake libspdlog-dev
    ```
3. Install project [prerequisites](https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c#install-gstreamer-on-ubuntu-or-debian)
    ```bash
    sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
    ```
4. Install this project
    ```bash
    git clone <this repository URL>
    ```
5. Inside Visual Studio Code
    - Click on `File > Open Workspace from File...`
    - Navigate to `robot.code-workspace`
    - Open it
6. You've installed the project 🎉

## Compile & run
1. Navigate to the installed project directory through WSL
2. Run `build.sh` script
3. Inside the `build` directory there would be `Robot` executable
