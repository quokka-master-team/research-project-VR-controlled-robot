FROM debian:stable-slim AS build-stage

# Install prerequisites
RUN apt-get update && \
    apt-get install -y build-essential cmake libspdlog-dev libasio-dev libgstreamer1.0-dev libyaml-cpp-dev libgstrtspserver-1.0-dev \
    libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad  gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa \
    gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio

# Copy only necessary files and set working dir
COPY /include /app/include
COPY /src /app/src
COPY CMakeLists.txt /app

# Build project
WORKDIR /app
RUN cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
RUN make --directory=build -j$(nproc) -s

# Final stage
FROM debian:stable-slim AS final-stage
COPY --from=build-stage /app/build/Camera ./Camera
COPY config.yaml .

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    libspdlog-dev libasio-dev libyaml-cpp-dev libgstrtspserver-1.0-dev \
    gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl \
    gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio

# Expose port
EXPOSE 3000

# Execute this project
ENTRYPOINT ["./Camera"]
