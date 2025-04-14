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


def main():
    x, y = load_dataset()


if __name__ == "__main__":
    main()
