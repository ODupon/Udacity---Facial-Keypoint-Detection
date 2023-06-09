## TODO: define the convolutional neural network architecture

import torch
import torch.nn as nn
import torch.nn.functional as F
# can use the below import should you choose to initialize the weights of your Net
import torch.nn.init as I


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        
        ## TODO: Define all the layers of this CNN, the only requirements are:
        ## 1. This network takes in a square (same width and height), grayscale image as input
        ## 2. It ends with a linear layer that represents the keypoints
        ## it's suggested that you make this last layer output 136 values, 2 for each of the 68 keypoint (x, y) pairs
        
        # As an example, you've been given a convolutional layer, which you may (but don't have to) change:
        # 1 input image channel (grayscale), 32 output channels/feature maps, 5x5 square convolution kernel
        ## output size = (W-F)/S +1 = (224-4)/1 +1 = 221
        # the output Tensor for one image, will have the dimensions: (20, 221, 221)
        self.conv1 = nn.Conv2d(1, 16, 4)
        # after one pool layer, this becomes (20, 110, 110)
        self.pool1 = nn.MaxPool2d(2,2)
        # dropout with p=0.4
#         self.conv1_drop = nn.Dropout(p=0.3)
        
        # 32 input image channel (grayscale), 64 output channels/feature maps, 4x4 square convolution kernel
        ## output size = (W-F)/S +1 = (110-3)/1 +1 = 108
        # the output Tensor for one image, will have the dimensions: (40, 108, 108)
        self.conv2 = nn.Conv2d(16,32,3)
        # after one pool layer, this becomes (40, 53, 53)
        self.pool2 = nn.MaxPool2d(2,2)
        # dropout with p=0.4
#         self.conv2_drop = nn.Dropout(p=0.3)
        
        # 64 input image channel (grayscale), 128 output channels/feature maps, 3x3 square convolution kernel
        ## output size = (W-F)/S +1 = (53-2)/1 +1 = 52
        # the output Tensor for one image, will have the dimensions: (60, 52, 52)
        self.conv3 = nn.Conv2d(32,48,2)
        # after one pool layer, this becomes (60, 26, 26)
        self.pool3 = nn.MaxPool2d(2,2)
        # dropout with p=0.4
#         self.conv3_drop = nn.Dropout(p=0.3)
        
        # 128 input image channel (grayscale), 256 output channels/feature maps, 2x2 square convolution kernel
        ## output size = (W-F)/S +1 = (26-1)/1 +1 = 26
        # the output Tensor for one image, will have the dimensions: (80, 26, 26)
        self.conv4 = nn.Conv2d(48,64,1)
        # after one pool layer, this becomes (80, 13, 13)
        self.pool4 = nn.MaxPool2d(2,2)
        # dropout with p=0.4
#         self.conv4_drop = nn.Dropout(p=0.6)
        
#         # 256 input image channel (grayscale), 512 output channels/feature maps, 1x1 square convolution kernel
#         ## output size = (W-F)/S +1 = (12-1)/1 +1 = 12
#         # the output Tensor for one image, will have the dimensions: (512, 12, 12)
#         self.conv5 = nn.Conv2d(256,512,1)
#         # after one pool layer, this becomes (512, 6, 6)
#         self.pool5 = nn.MaxPool2d(2,2)
#         # dropout with p=0.4
#         self.conv5_drop = nn.Dropout(p=0.6)
        
#         # 256 input image channel (grayscale), 512 output channels/feature maps, 1x1 square convolution kernel
#         ## output size = (W-F)/S +1 = (6-1)/1 +1 = 6
#         # the output Tensor for one image, will have the dimensions: (512, 6, 6)
#         self.conv6 = nn.Conv2d(512,1024,1)
#         # after one pool layer, this becomes (1024, 3, 3)
#         self.pool6 = nn.MaxPool2d(2,2)
#         # dropout with p=0.4
#         self.conv6_drop = nn.Dropout(p=0.6)
        
        # 512 outputs * the 6*6 filtered/pooled map size
        self.fc1 = nn.Linear(64*13*13, 6760)
        # dropout with p=0.4
        self.fc1_drop = nn.Dropout(p=0.5)
        
        self.fc2 = nn.Linear(6760, 1000)
        # dropout with p=0.4
        self.fc2_drop = nn.Dropout(p=0.5)
        
        self.fc3 = nn.Linear(1000, 136)

        ## Note that among the layers to add, consider including:
        # maxpooling layers, multiple conv layers, fully-connected layers, and other layers (such as dropout or batch normalization) to avoid overfitting
        
    def forward(self, x):
        ## TODO: Define the feedforward behavior of this model
        ## x is the input image and, as an example, here you may choose to include a pool/conv step:
        ## x = self.pool(F.relu(self.conv1(x)))
        
        # Defining the 5 convolutional layers
        
        x = self.pool1(F.relu(self.conv1(x)))
#         x = self.conv1_drop(x)
        
        x = self.pool2(F.relu(self.conv2(x)))
#         x = self.conv2_drop(x)
        
        x = self.pool3(F.relu(self.conv3(x)))
#         x = self.conv3_drop(x)
        
        x = self.pool4(F.relu(self.conv4(x)))
#         x = self.conv4_drop(x)
        
#         x = self.pool5(F.relu(self.conv5(x)))
#         x = self.conv5_drop(x)
        
#         x = self.pool6(F.relu(self.conv6(x)))
#         x = self.conv6_drop(x)
        
        # prep for the 3 linear layers
        # this line of code is the equivalent of Flatten in Keras
        x = x.view(x.size(0), -1)
        
        x = F.relu(self.fc1(x))
        x = self.fc1_drop(x)
        
        x = F.relu(self.fc2(x))
        x = self.fc2_drop(x)
        
#         x = F.relu(self.fc3(x))
#         x = self.fc3_drop(x)
        
        x = self.fc3(x)
        
        # a modified x, having gone through all the layers of your model, should be returned
        return x