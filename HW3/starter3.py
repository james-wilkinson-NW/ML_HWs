import sys
import random
import math
import numpy as np
import torch
import torch.nn.functional as F
import torch.nn as nn
from torch.autograd import Variable
from NN import FeedForward, trainNN
from torch.utils.data import DataLoader


def read_mnist(file_name):
    data_set = []
    with open(file_name, 'rt') as f:
        for line in f:
            line = line.replace('\n', '')
            tokens = line.split(',')
            label = tokens[0]
            attribs = []
            for i in range(784):
                attribs.append(tokens[i + 1])
            data_set.append([label, attribs])
    return (data_set)


def show_mnist(file_name, mode):
    data_set = read_mnist(file_name)
    for obs in range(len(data_set)):
        for idx in range(784):
            if mode == 'pixels':
                if data_set[obs][1][idx] == '0':
                    print(' ', end='')
                else:
                    print('*', end='')
            else:
                print('%4s ' % data_set[obs][1][idx], end='')
            if (idx % 28) == 27:
                print(' ')
        print('LABEL: %s' % data_set[obs][0], end='')
        print(' ')


def read_insurability(file_name):
    count = 0
    data = []
    with open(file_name, 'rt') as f:
        for line in f:
            if count > 0:
                line = line.replace('\n', '')
                tokens = line.split(',')
                if len(line) > 10:
                    x1 = float(tokens[0])
                    x2 = float(tokens[1])
                    x3 = float(tokens[2])
                    if tokens[3] == 'Good':
                        cls = 0
                    elif tokens[3] == 'Neutral':
                        cls = 1
                    else:
                        cls = 2
                    data.append([[cls], [x1, x2, x3]])
            count = count + 1
    return (data)


def classify_insurability():
    train = read_insurability('three_train.csv')
    valid = read_insurability('three_valid.csv')
    test = read_insurability('three_test.csv')

    #convert data to DataLoader objects for batch processing
    trainDL = DataLoader(train, batch_size=50,shuffle=True)
    validDL = DataLoader(valid, batch_size=50,shuffle=True)
    testDL = DataLoader(test, batch_size=50,shuffle=True)

    # insert code to train simple FFNN and produce evaluation metrics
    NN = FeedForward(3, 3, hiddenNs=[2])  # 3 inputs, 2 hidden, 3 outputs as per slides 11-8

    loss_func = nn.MSELoss()
    print("params: ",list(NN.parameters()))
    optimizer = torch.optim.SGD(NN.parameters(), lr=1e-4, momentum=0.1)
    train_loss = []
    epoch = 0 #counter for which epoch we're in
    losses = 1e8
    while losses > 1e-2 and epoch < 50:
        epoch += 1
        print(f"Epoch {epoch}\n------------------------------- \n")
        losses = trainNN(train, NN, loss_func, optimizer)
        train_loss.append(losses)
    print(train_loss)

def classify_mnist():
    train = read_mnist('mnist_train.csv')
    valid = read_mnist('mnist_valid.csv')
    test = read_mnist('mnist_test.csv')
    show_mnist('mnist_test.csv', 'pixels')

    # insert code to train a neural network with an architecture of your choice
    # (a FFNN is fine) and produce evaluation metrics


def classify_mnist_reg():
    train = read_mnist('mnist_train.csv')
    valid = read_mnist('mnist_valid.csv')
    test = read_mnist('mnist_test.csv')
    show_mnist('mnist_test.csv', 'pixels')

    # add a regularizer of your choice to classify_mnist()


def classify_insurability_manual():
    train = read_insurability('three_train.csv')
    valid = read_insurability('three_valid.csv')
    test = read_insurability('three_test.csv')

    # reimplement classify_insurability() without using a PyTorch optimizer.
    # this part may be simpler without using a class for the FFNN


def main():
    classify_insurability()
    #classify_mnist()
    #classify_mnist_reg()
    #classify_insurability_manual()


if __name__ == "__main__":
    main()
