# Image-Overlay
Python implementation of shape detection and image overlaying from a given video using Image Processing
Inputs a video and detects the shape and color of object in the video -- Further , using overlaying methods , overlay (add) a flower on the centroid of the object og type depending on the shape and color of object ..

Further, only new object that comes to the screen is detected , and old object is not overlayed any further.

2 output files created : 1. A csv file "results.csv" depicting the shape, color and centroid of objects detected in video
                        2. An output video file "video_output.mp4" showing the output overlay results.
                        
Note: * Sample Video provided "Video.mp4".
      * A delay is provided between shape detection and actual overlay on the shape.
      * Colors that can be detected - Red, Blue, Green
      * Shapes that can be detected - Triangle , Rhombus , Trapezium , Pentagon , Hexagon , Circle.
