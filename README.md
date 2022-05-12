# SMDV
The following is a proposed computer vision-based model for video frame summarization of important events to allow video reviewing faster by first detecting the moving objects in a stationary background so that they are superimposed and displayed simultaneously on a new video file. The problem targeted is that forensic investigators spend long periods of time watching CCTV footage in order to look for evidence for a case. However, some videos include long footage of a stationary background with few important events such as people or cars passing by. Therefore, this model will remove all the unnecessary footage and overlay the important footage so that the viewer can focus on the important parts of the video while at the same time saving time. For this, two different models are needed, one for the movement detection and another one for the object superimposition. Since the priority for the object detection is accuracy over speed, it is critical that we use an advanced multi-stage detector for the SDMV model.

Visual Explanation of SDMV model
![image](https://user-images.githubusercontent.com/57282069/168065072-599732b5-e813-483d-ac92-b964a9a5d080.png)



Flowchart
![flowchart](https://user-images.githubusercontent.com/57282069/168064974-e1b6f8af-7323-4212-ac4f-563dabaab189.png)
