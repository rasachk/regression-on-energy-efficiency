import numpy as np
import csv


def load_dataset():
    data = []
    with open('energy_efficiency_data.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if len(row) < 9:
                continue
            try:
                features = [float(x) for x in row[:8]]
                target = float(row[8])
                data.append(features + [target])
            except ValueError:
                continue

    data = np.array(data)
    x = data[:, :8]
    y = data[:, 8]
    return x, y


def split_data(x, y, train_ratio):
    indices = np.arange(x.shape[0])
    np.random.shuffle(indices)
    train_size = int(len(x) * train_ratio)
    train_idx = indices[:train_size]
    test_idx = indices[train_size:]
    return x[train_idx], y[train_idx], x[test_idx], y[test_idx]


def main():
    x, y = load_dataset()
    x_train, y_train, x_test, y_test = split_data(x, y, 0.8)


if __name__ == "__main__":
    main()
