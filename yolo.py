from transformers import AutoImageProcessor, AutoModelForObjectDetection
import torch
from matplotlib.pyplot import imshow
from PIL import Image,ImageDraw
import requests
import os
import cv2
import numpy as np
image_processor = AutoImageProcessor.from_pretrained("hustvl/yolos-tiny")
model = AutoModelForObjectDetection.from_pretrained("hustvl/yolos-tiny")

def yolo_box(image_folder,img_path):
  # url = "http://images.cocodataset.org/val2017/000000039769.jpg"
  # image = Image.open(requests.get(url, stream=True).raw)
  # print(image_path)
  image=Image.open(image_folder+"-opencv/"+ img_path)
  # imshow(np.asarray(image))
  
  inputs = image_processor(images=image, return_tensors="pt")
  outputs = model(**inputs)

  # convert outputs (bounding boxes and class logits) to COCO API
  target_sizes = torch.tensor([image.size[::-1]])
  results = image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[
      0
  ]

  for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
      box = [round(i, 2) for i in box.tolist()]
      
      xc,yc,nw,nh=box
      top_left=(int(xc),int(yc))
      top_right=(int(nw),int(nh))

      img1 = ImageDraw.Draw(image)  
      img1.rectangle((top_left,top_right), outline ="white", width=5) 
      img1.text(top_left, f"{model.config.id2label[label.item()]}", fill="white")

      # image.show()
      # print(
      #     f"Detected {model.config.id2label[label.item()]} with confidence "
      #     f"{round(score.item(), 3)} at location {box}"
      # )
  image=cv2.cvtColor(np.asarray(image,dtype=np.float32), cv2.COLOR_RGB2BGR)
  cv2.imwrite(os.path.join(f'{image_folder}-opencv', f"{img_path}"), image)