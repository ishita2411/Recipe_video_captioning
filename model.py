import torch
from tqdm import tqdm
from torchvision import models
import torch.nn as nn
import torchvision.transforms as transforms
# for this prototype we use no gpu, cuda= False and as model resnet18 to obtain feature vectors
class Img2VecResnet18(nn.Module):
    def __init__(self,device):
        super(Img2VecResnet18, self).__init__()
        self.device=device
        self.numberFeatures = 512
        self.modelName = "resnet-18"
        self.model,self.featureLayer = self.__getFeatureLayer()
        self.model = self.model.to(device)
        self.model.eval()
        self.toTensor = transforms.ToTensor()
        
        # normalize the resized images as expected by resnet18
        # [0.485, 0.456, 0.406] --> normalized mean value of ImageNet, [0.229, 0.224, 0.225] std of ImageNet
        self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        
    def getVec(self, img):
        image = self.normalize(self.toTensor(img)).unsqueeze(0).to(self.device)
        embedding = torch.zeros(1, self.numberFeatures, 1, 1)

        def copyData(m, i, o): embedding.copy_(o.data)

        h = self.featureLayer.register_forward_hook(copyData)
        self.model(image)
        h.remove()

        return embedding.numpy()[0, :, 0, 0]

    def __getFeatureLayer(self):
        
        cnnModel = models.resnet18(pretrained=True)
        layer = cnnModel._modules.get('avgpool')
        self.layer_output_size = 512
        
        return cnnModel, layer
        


