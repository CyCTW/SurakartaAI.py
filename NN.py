import torch
import torch.nn as nn
import torch.nn.functional as F

class CNNImpl(nn.Module):
  def __init__(self):
    super(CNNImpl, self).__init__()
    self.conv1 = nn.Conv2d(1, 64, 3, stride=1, padding=1)
    self.conv2 = nn.Conv2d(64, 128, 3, stride=1, padding=1)
    self.conv3 = nn.Conv2d(128, 256, 3, stride=1, padding=1)
      
    self.bn1 = nn.BatchNorm2d(128)
    self.bn2 = nn.BatchNorm2d(256) 

    self.fc1 = nn.Linear(256*6*6, 1024)
    self.fc2 = nn.Linear(1024, 512)
    self.fc3 = nn.Linear(512, 1)
  
  def forward(self, s):
    s = F.relu(self.conv1(s))
    s = F.relu(self.bn1(self.conv2(s)))
    s = F.relu(self.bn2(self.conv3(s)))
    s = s.view(s.size()[0], -1)
    s = F.relu(self.fc1(s))
    s = F.relu(self.fc2(s))
    s = self.fc3(s)

    return F.tanh(s)

Net = CNNImpl()
 
def generate_states(data, next):
  for i in range(36):
    p = next[i]
    if p == 0:
      data[0][i] = 0
    elif p == 1:
      data[0][i] = 1
    else:
      data[0][i] = -1
  return