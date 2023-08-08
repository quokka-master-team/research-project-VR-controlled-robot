# Tutorial

## Installation
1. Install **Ubuntu** distribution on your WSL 2 from cmd
    ```batch
    wsl --install ubuntu
    ```
2. Open Visual Studio Code and install the [WSL extension](https://code.visualstudio.com/docs/remote/wsl-tutorial#_install-the-extension)
3. Connect to the Ubuntu from VSCode (left-bottom icon `><`)
4. Open terminal inside the IDE
5. Update the Ubuntu
    ```bash
    sudo apt-get update
    sudo apt-get upgrade
    ```
6. Install packages
    ```bash
    sudo apt-get install build-essential cmake
    ```
7. Install this project
    ```bash
    git clone <this repository URL>
    ```
8. Inside Visual Studio Code
    - Click on `File > Open Workspace from File...`
    - Navigate to `robot.code-workspace`
    - Open it
9. You've installed the project 🎉

## Compile & run
1. Navigate to the installed project directory through WSL
2. Run `build.sh` script
3. Inside the `out` directory there would be `Robot` executable
