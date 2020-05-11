import torch
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data.dataset import Dataset

from NN import generate_states, Net
from Episode import Episode



class BoardDataSet(Dataset):
  def __init__(self, states, labels, transform = None):
    self.states = states
    self.labels = labels
    self.transform = transform
  
  def __getitem__(self, index):
    nextb = self.states[index]
    tensor_stack = torch.FloatTensor(1, 36).zero_()

    generate_states(tensor_stack, nextb)

    state_tensor = tensor_stack.view(1, 6, 6)

    label = self.labels[index]
    label_tensor = torch.full((1, 36), label, dtype=torch.float32)

    return state_tensor, label_tensor

  def __len__(self):
    return len(self.states)

def train_net(game, num_epoch=10):

  dataset = BoardDataSet(game.train_boards, game.train_result)
  data_loader = torch.utils.data.DataLoader(dataset, batch_size = 64, num_workers = 2) # workers

  optimizer = optim.Adam(Net.parameters(), lr = 0.001)

  print("Start training")

  for i in range(1, 11):
    mse = 0.0
    batch_num = 0

    for state, label in data_loader:
      boards_ = state
      labels_ = label.squeeze()

      output = Net.forward(boards_)

      loss = F.mse_loss(output, labels_)

      optimizer.zero_grad()
      loss.backward()
      optimizer.step()

      mse += loss.item()
      loss.item()
      batch_num += 1
    mse /= batch_num
    print("Epoch: " + str(i) + " : " +"Mean square error: " + str(mse) )

