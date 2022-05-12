## <div align="center">SMDV</div>

The following is a proposed computer vision-based model for video frame summarization of important events to allow video reviewing faster by first detecting the moving objects in a stationary background so that they are superimposed and displayed simultaneously on a new video file. The problem targeted is that forensic investigators spend long periods of time watching CCTV footage in order to look for evidence for a case. However, some videos include long footage of a stationary background with few important events such as people or cars passing by. Therefore, this model will remove all the unnecessary footage and overlay the important footage so that the viewer can focus on the important parts of the video while at the same time saving time. For this, two different models are needed, one for the movement detection and another one for the object superimposition. Since the priority for the object detection is accuracy over speed, it is critical that we use an advanced multi-stage detector for the SDMV model.


<details open>
<summary>Visual Explanation of SDMV model</summary>

![image](https://user-images.githubusercontent.com/57282069/168068056-a8d1f6e9-ace8-4644-886b-fc2f76ba4e87.png)


</details>

<details open>
<summary>Flowchart</summary>
  
![flowchart](https://user-images.githubusercontent.com/57282069/168068028-2221b2b4-b9a8-40ce-8018-2a64bb157767.png)


</details>
