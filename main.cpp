#include <gst/gst.h>

int main(int argc, char *argv[])
{
    gst_init(&argc, &argv);

    // Create pipeline
    GstElement *pipeline = gst_parse_launch("v4l2src ! videoconvert ! x264enc ! rtph264pay ! tcpserversink host=0.0.0.0 port=1234", NULL);

    if (!pipeline) {
        g_print("Failed to create pipeline\n");
        return -1;
    }
    g_print("Pipeline created successfully\n");

	// Check if the camera source element is present
    GstElement *cameraSrc = gst_bin_get_by_name(GST_BIN(pipeline), "v4l2src");
    if (!cameraSrc) {
        g_print("Camera source element not found\n");
        return -1;
    }

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
