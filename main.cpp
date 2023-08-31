#include <gst/gst.h>

int main(int argc, char *argv[])
{
    gst_init(&argc, &argv);

    // Create pipeline
    GstElement *pipeline = gst_parse_launch("v4l2src device=/dev/video0 ! videoconvert ! autovideosink", NULL); // It should work.
    // If not, try: gst-launch-1.0 v4l2src device=/dev/video0 ! 'image/jpeg, width=640, height=480, format=MJPG' ! jpegdec ! autovideosink

    if (!pipeline) {
        g_print("Failed to create pipeline\n");
        return -1;
    }
    g_print("Pipeline created successfully\n");

    // Start playing
    GstStateChangeReturn ret = gst_element_set_state(pipeline, GST_STATE_PLAYING);
    if (ret == GST_STATE_CHANGE_FAILURE) {
        g_print("Failed to start playing\n");
        return -1;
    }
    g_print("Pipeline started playing\n");

    // Main loop
    GMainLoop *loop = g_main_loop_new(NULL, FALSE);
    g_main_loop_run(loop);

    // Clean up
    gst_element_set_state(pipeline, GST_STATE_NULL);
    gst_object_unref(GST_OBJECT(pipeline));
    g_main_loop_unref(loop);

    return 0;
}
