import requests
from PIL import Image
import torch
import cv2
from transformers import BlipProcessor, BlipForConditionalGeneration

def get_model(config,device):
  processor = BlipProcessor.from_pretrained(config["processor"])
  model = BlipForConditionalGeneration.from_pretrained(config["model"]).to(device)
  return processor, model

def image_caption(processor, model, image_folder,image_path,device):
  raw_image = Image.open(image_folder+"-opencv/"+ image_path)
  inputs = processor(raw_image, return_tensors="pt").to(device)
  out = model.generate(**inputs)
  return processor.decode(out[0], skip_special_tokens=True)

def get_captions(final_frames, processor, model,device):
  output = {}
  for k, v in final_frames.items():
    image_folder = k
    caption =""
    for k1, v1 in v.items():
      caption = caption + image_caption(processor, model, image_folder, v1,device) +". "
    output[image_folder] = caption
  return output