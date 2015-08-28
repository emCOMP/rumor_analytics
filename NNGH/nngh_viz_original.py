from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


def main(
    path,
    cutoff,
    data_columns):

    df = pd.DataFrame.from_csv(path, index_col=False)

    # Clean the data to take out components with less
    # than CUTOFF rumor related tweets.
    sums = df[data_columns].sum(axis=1)
    df = df[sums > cutoff]

    # Create a grid with the coodinates for the tiles.
    # (Each column of tiles has identical height)
    y, x = np.mgrid[0:len(data_columns) + 1, 0:1]

    # Transform the width of each column by the size
    # of the corresponding component.
    size = np.array(list(df['size']))

    x = [0.]
    x_labels = []
    prev = 0.
    for v in size:
        current = prev + v
        x.append(current)
        x_labels.append(prev + (v / 2))
        prev = current

    x = np.array(x)
    # Get the counts for each tile.
    # Take the log.
    data = df[data_columns]
    # Clip the zero values since we're taking the log.
    data = data.clip_lower(1)
    data = data.apply(np.log10)
    data = data.fillna(0).values

    # Plot it
    fig, ax = plt.subplots()
    plt.pcolormesh(x, y, data.T,
                   cmap='Blues',
                   edgecolors=[0.9, 0.9, 0.9],
                   vmin=data.min(),
                   vmax=data.max()
                   )
    plt.axis([x.min(), x.max(), y.min(), y.max()])
    plt.title('Top Level Component-Tweet Distribution')
    plt.xlabel('Component\n(Label and Width Indicate Component Size)\n')
    plt.xticks(
        x_labels,
        [x for x in df['component']],
        rotation='vertical'
        )
    plt.ylabel('Rumor')
    plt.yticks(np.arange(len(data_columns)) + 0.5, data_columns)
    for tic in ax.yaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
    cb = plt.colorbar()
    cb.set_label('Rumor Tweet Count\n(log10 scale)')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Visualizes NNGH Accuracy Results')
    parser.add_argument(
        'accuracy_data', help='Path to the dataset (csv on disk)',
        type=str)
    # sydney_processed
    parser.add_argument(
        '-cut', '--cutoff', help='The minimum number of rumor tweets which must be included in a component for it to appear in the visual.',
        type=int, default=10)
    # mongo_id
    parser.add_argument(
        '-sc','--split_column', help='The name of the label column to use for chunking.',
        type=str, default='time')
    parser.add_argument(
        '-dc', '--count_columns', help='Which columns in the dataframe contain ',
        type=str, nargs='*', default=['flag', 'suicide', 'hadley', 'lakemba', 'airspace'])

    args = parser.parse_args()
    main(args.accuracy_data, args.cutoff, args.count_columns)
