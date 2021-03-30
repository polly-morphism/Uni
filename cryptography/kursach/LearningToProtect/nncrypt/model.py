import torch
import torch.nn as nn
import torch.nn.functional as F


class Alice(nn.Module):
    def __init__(self, hp):
        super(Alice, self).__init__()
        self.depth = hp.alice.depth
        self.hidden = hp.alice.hidden

        self.mlp = nn.ModuleList(
            [nn.Linear(hp.data.plain + hp.data.key, self.hidden)]
            + [nn.Linear(self.hidden, self.hidden) for _ in range(self.depth - 1)]
        )
        self.last = nn.Linear(self.hidden, hp.data.cipher)

    def forward(self, p, k):
        print("Alice's forward")
        print("Input p={}, k={}".format(p, k))
        x = torch.cat((p, k), dim=-1)

        for idx, layer in enumerate(self.mlp):
            if idx == 0:
                x = F.relu(layer(x))
            else:
                x = F.relu(x + layer(x))

        x = torch.tanh(self.last(x))
        print("Output calculated by Alice {}".format(x))
        return x


class Bob(nn.Module):
    def __init__(self, hp):
        super(Bob, self).__init__()
        self.depth = hp.bob.depth
        self.hidden = hp.bob.hidden

        self.mlp = nn.ModuleList(
            [nn.Linear(hp.data.cipher + hp.data.key, self.hidden)]
            + [nn.Linear(self.hidden, self.hidden) for _ in range(self.depth - 1)]
        )
        self.last = nn.Linear(self.hidden, hp.data.plain)

    def forward(self, c, k):
        print("Bob's forward")
        print("Input c={}, k={}".format(c, k))

        x = torch.cat((c, k), dim=-1)

        for idx, layer in enumerate(self.mlp):
            if idx == 0:
                x = F.relu(layer(x))
            else:
                x = F.relu(x + layer(x))

        x = torch.tanh(self.last(x))
        print("Output calculated by Bob {}".format(x))
        return x


class Eve(nn.Module):
    def __init__(self, hp):
        super(Eve, self).__init__()
        self.depth = hp.eve.depth
        self.hidden = hp.eve.hidden

        self.mlp = nn.ModuleList(
            [nn.Linear(hp.data.cipher, self.hidden)]
            + [nn.Linear(self.hidden, self.hidden) for _ in range(self.depth - 1)]
        )
        self.last = nn.Linear(self.hidden, hp.data.plain)

    def forward(self, c):
        print("Eve's forward")
        print("Input c={}".format(c))

        x = c

        for idx, layer in enumerate(self.mlp):
            if idx == 0:
                x = F.relu(layer(x))
            else:
                x = F.relu(x + layer(x))

        x = torch.tanh(self.last(x))
        print("Output calculated by Eve", x)
        return x
