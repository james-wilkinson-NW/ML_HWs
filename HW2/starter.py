import math


# formats the elements in "list" to conform to a data type
def format_list(list, dtype_func):
    return [dtype_func(i) for i in list]


# returns dot product of vectors a,b
def dot(a, b):
    assert (len(a) == len(b))
    N = len(a)
    return sum([a[i] * b[i] for i in range(N)])


# returns most frequent element in a list
def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i
    return num


# returns magnitude of vector a
def mag(a):
    return math.sqrt(sum([x ** 2 for x in a]))


# returns Euclidean distance between vectors a dn b
def euclidean(a, b):
    assert (len(a) == len(b))
    N = len(a)
    dist2 = sum([(a[i] - b[i]) ** 2 for i in range(N)])
    dist = math.sqrt(dist2)
    return (dist)


# returns Cosine Similarity between vectors a dn b
def cosim(a, b):
    dist = dot(a, b) / (mag(a) * mag(b))
    return (dist)


# returns a list of labels for the query dataset based upon labeled observations in the train dataset.
# metric is a string specifying either "euclidean" or "cosim".  
# All hyper-parameters should be hard-coded in the algorithm.
def knn(train, query, metric):
    k = 5  # number of nearest neighbors to look at

    if metric == "euclidean":
        metric_func = euclidean
    elif metric == "cosim":
        metric_func = cosim
    else:
        raise NameError("Invalid Metric choice")

    labels = []
    for testpoint in query:
        traincopy = train.copy()
        dists = []

        for labelledpoint in train:
            dists.append(metric_func(testpoint[1], labelledpoint[1]))

        all_labels = []
        while len(all_labels) < k:
            next_nearest_index = dists.index(min(dists))  # index of the nearest training point
            all_labels.append(traincopy[next_nearest_index][0])
            # now remove the smallest value from dists and train
            traincopy.pop(next_nearest_index)
            dists.pop(next_nearest_index)

        label = most_frequent(all_labels)
        labels.append(label)

    return (labels)


# returns a list of labels for the query dataset based upon observations in the train dataset.
# labels should be ignored in the training set
# metric is a string specifying either "euclidean" or "cosim".  
# All hyper-parameters should be hard-coded in the algorithm.
def kmeans(train, query, metric):
    return (labels)


def read_data(file_name):
    data_set = []
    with open(file_name, 'rt') as f:
        for line in f:
            line = line.replace('\n', '')
            tokens = line.split(',')
            label = float(tokens[0])
            attribs = []
            for i in range(784):
                attribs.append(tokens[i + 1])
            data_set.append([label, format_list(attribs, float)])
    return (data_set)


def show(file_name, mode):
    data_set = read_data(file_name)
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


# returns the accuracy of a set of guesses to the expected values
def accuracy(guess_labels,true_labels):
    assert(len(guess_labels) == len(true_labels))
    N = len(guess_labels)
    return sum([int(guess_labels[i]==true_labels[i]) for i in range(N)])


def main():
    # show('valid.csv', 'pixels')
    train = read_data('train.csv')
    valid = read_data('valid.csv')
    test = read_data('test.csv')
    labels = knn(train, test, "euclidean")
    true_labels = [x[0] for x in test]
    _accuracy = accuracy(labels,true_labels)
    print('accuracy: ', _accuracy)


if __name__ == "__main__":
    main()
