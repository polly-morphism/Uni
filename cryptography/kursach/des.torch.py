from Crypto.Cipher import DES
from Crypto import Random
from Crypto.Util import Counter
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable

np.random.seed(10)


def unhex_str(hes_str):
    return int(hes_str, 16).to_bytes(len(hes_str) // 2, "big")


def bin_to_b(bin):
    n = 0
    for bit in range(64):
        n <<= 1
        if bin[bit] >= 0.5:
            n += 1

    return n.to_bytes(8, "big")


def b_to_bin(b):
    n = int.from_bytes(b, "big")
    bin = np.zeros(64, dtype=int)
    for bit in range(64):
        bin[63 - bit] = n & 1
        n >>= 1

    return bin


class CascadeNet(nn.Module):
    def __init__(self, hidden_sizes):
        super(CascadeNet, self).__init__()
        self.linears = nn.ModuleList()
        hidden_sizes = [64] + hidden_sizes
        hidden_sizes = hidden_sizes + list(reversed(hidden_sizes))
        for i in range(len(hidden_sizes) - 1):
            self.linears.append(nn.Linear(sum(hidden_sizes[:i+1]), hidden_sizes[i + 1]))

    def forward(self, x):
        prev_inputs = [x]
        for i in range(len(self.linears)):
            input = torch.cat(prev_inputs, dim=1)
            #print(input.shape, self.linears[i])
            x = self.linears[i](input)
            if i < len(self.linears) - 1:
                #x = F.sigmoid(x)
                x = F.tanh(x)
                #x = F.relu(x)

            prev_inputs.append(x)

        return x
        #return F.sigmoid(x)


def make_io(num, cipher):
    inputs = (np.random.randint(0, 2, (num, 64))).astype(np.float32)
    outputs = np.zeros_like(inputs)
    for bi in range(num):
        outputs[bi, :] = b_to_bin(cipher.encrypt(bin_to_b(inputs[bi, :])))

    inputs = torch.from_numpy(inputs).cuda()
    outputs = torch.from_numpy(outputs).cuda()
    return outputs, inputs


key = unhex_str("0E329232EA6D0D73")
cipher = DES.new(key, DES.MODE_ECB)
plaintext = unhex_str("8787878787878787")
msg = cipher.encrypt(plaintext)
print("ct", msg)
deciphered = cipher.decrypt(msg)
print("pt", deciphered)


b = bin_to_b(np.random.randint(0, 2, 64))
cipher = DES.new(b, DES.MODE_ECB)
print(b, cipher.encrypt(b), cipher.decrypt(b))
print(b, b_to_bin(b), bin_to_b(b_to_bin(b)))

successes = 0
for trial in range(1000):
    batch_size = 2048
    print_period = 10000
    train_data_size = 2048
    model = CascadeNet([128, 512])
    model = model.cuda()
    #optimizer = optim.SGD(model.parameters(), lr=1e-5, momentum=0.999)
    optimizer = optim.Adam(model.parameters(), lr=1e-4)
    #loss = nn.BCEWithLogitsLoss()
    loss = nn.MSELoss()

    key = bin_to_b(np.random.randint(0, 2, 64))
    cipher = DES.new(key, DES.MODE_ECB)
    average_loss = 0

    train_input, train_output = make_io(train_data_size, cipher)
    test_input, test_output = make_io(10000, cipher)
    batch_order = np.array(range(train_data_size))

    for epoch in range(10000):
        np.random.shuffle(batch_order)
        batch_order_t = torch.from_numpy(batch_order).cuda()
        cum_loss = 0
        for batch_idx in range(train_data_size // batch_size):
            inputs = Variable(train_input[batch_order_t[batch_idx * batch_size : (batch_idx + 1) * batch_size]],
                              requires_grad=False)

            outputs = Variable(train_output[batch_order_t[batch_idx * batch_size : (batch_idx + 1) * batch_size]],
                              requires_grad=False)

            model.zero_grad()
            preds = model(inputs)
            l = loss(preds, outputs)
            l.backward()
            optimizer.step()
            ln = l.data.cpu().numpy()
            cum_loss += ln

        train_loss = cum_loss / (train_data_size // batch_size)
        if train_loss < 1e-4:
            print("train loss %f is acceptable after %d epochs" % (train_loss, epoch))
            break

        if epoch > 0 and epoch % print_period == 0:
            print("epoch %d, train loss %f" % (epoch, train_loss))

    if epoch == 9999:
        print("training failed to converge, loss %f" % train_loss)

    inputs = Variable(test_input, requires_grad=False)
    outputs = Variable(test_output, requires_grad=False)
    preds = model(inputs)
    l = loss(preds, outputs)
    val_loss = l.data.cpu().numpy()
    succ = val_loss < 0.25
    if succ:
        successes += 1

    print("trial %d. losses: train %f, val %f: %s" % (trial, train_loss, val_loss, "SUCCESS" if succ else "FAIL"))

print("Total successes: %d / 1000" % successes)
