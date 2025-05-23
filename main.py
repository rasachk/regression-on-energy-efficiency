import numpy as np
import csv
from itertools import combinations_with_replacement
import matplotlib.pyplot as plt


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


def compute_basis(dataset, degree):
    n_samples, n_features = dataset.shape
    phi = np.ones((n_samples, 1))
    for d in range(1, degree + 1):
        combs_d = combinations_with_replacement(range(n_features), d)
        for comb in combs_d:
            new_feature = np.prod(dataset[:, comb], axis=1, keepdims=True)
            phi = np.hstack((phi, new_feature))
    return phi


def train_linear_regression(phi, dataset):
    return np.linalg.pinv(phi.T @ phi) @ phi.T @ dataset


def predict(phi, weight):
    return phi @ weight


def compute_rmsd(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))


def main():
    x, y = load_dataset()
    x_train, y_train, x_test, y_test = split_data(x, y, 0.8)

    degrees = range(1, 6)

    rmsd_train = []
    rmsd_test = []

    for degree in degrees:
        phi_train = compute_basis(x_train, degree)
        phi_test = compute_basis(x_test, degree)

        weight = train_linear_regression(phi_train, y_train)
        y_pred_train = predict(phi_train, weight)
        y_pred_test = predict(phi_test, weight)

        rmsd_train.append(compute_rmsd(y_train, y_pred_train))
        rmsd_test.append(compute_rmsd(y_test, y_pred_test))

        print(f"Degree {degree}: Train RMSD = {rmsd_train[-1]:.4f}, Test RMSD = {rmsd_test[-1]:.4f}")

    plt.figure(figsize=(10, 6))
    plt.plot(degrees, rmsd_train, marker='o', label='Train RMSD')
    plt.plot(degrees, rmsd_test, marker='s', label='Test RMSD')
    plt.xlabel('Polynomial Degree')
    plt.ylabel('RMSD')
    plt.title('RMSD vs Polynomial Degree (Heating Load Prediction)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plot_rmsd.png")
    plt.show()


if __name__ == "__main__":
    main()
