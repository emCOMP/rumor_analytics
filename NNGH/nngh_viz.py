from matplotlib import pyplot as plt
from nngh import NNGraphHierarchy
import numpy as np
import graphlab as gl
import graphlab.aggregate as agg


def main(path, output, radius, cutoff=None, logscale=False, width_by_size=False, include_unrelated=False):

    #m = NNGraphHierachy(path)
    #g = m.get_graph(radius)
    #sf = g.vertices
    sf = gl.SFrame('vis_test_dump')
    sf['rumor'] = sf['rumor'].fillna('None')
    rumors = list(sf['rumor'].unique())
    groups = sf.groupby(['hier_id', 'rumor'], {'tweets': agg.COUNT()})
    data = groups.unstack(['rumor', 'tweets'], 'rumor_tweets').unpack('rumor_tweets', limit=rumors, column_types=[int for r in rumors], column_name_prefix='')
    # Compute the size of each component
    data['size'] = data[rumors].apply(lambda x: sum([v for k,v in x.iteritems() if v]))
    if logscale:
        data['log_size'] = data['size'].clip_lower(1).apply(np.log10).fillna(0)
    data['rumor_tweets'] = data[[r for r in rumors if r != 'None']].apply(lambda x: sum([v for k,v in x.iteritems() if v]))
    rumor_only = data.dropna([r for r in rumors if r != 'None'], how='all')
    
    if cutoff:
        rumor_only = rumor_only[rumor_only['rumor_tweets'] >= cutoff]
    
    for r in rumors:
        data[r] = data[r].fillna(0)
        if logscale:
            data[r] = data[r].clip_lower(1).apply(np.log10).fillna(0)
        
        if r in rumor_only.column_names():
            rumor_only[r] = rumor_only[r].fillna(0)
            if logscale:
                rumor_only[r] = rumor_only[r].clip_lower(1).apply(np.log10).fillna(0)

    if not include_unrelated:
        rumors.remove('None')
    tmp = rumor_only[rumors]
    print tmp
    rumor_labels = [c for c in tmp.column_names() if c in rumors]
    z = rumor_only[rumors].to_numpy().T
    
    # Create a grid with the coodinates for the tiles.
    # (Each column of tiles has identical height)
    y, x = np.mgrid[0:z.shape[0] + 1, 0:z.shape[1] + 1]

    if width_by_size:
        if logscale:
            s = rumor_only['log_size']
        else:
            s = rumor_only['size']
        # Transform the width of each column by the size
        # of the corresponding component.
        x = [0.]
        x_labels = []
        prev = 0.
        for v in s:
            current = prev + v
            x.append(current)
            x_labels.append(prev + (v / 2))
            prev = current
        x = np.array(x)
    else:
        x_labels = x[0] + 0.5

    # Plot it
    fig, ax = plt.subplots()
    plt.pcolormesh(x, y, z,
                   cmap='Blues',
                   edgecolors=[0.9, 0.9, 0.9],
                   vmin=z.min(),
                   vmax=z.max()
                   )
    plt.axis([x.min(), x.max(), y.min(), y.max()])
    plt.title('Top Level Component-Tweet Distribution')
    plt.xlabel('Component\n(Label and Width Indicate Component Size)\n')
    x_label_text = list(rumor_only.apply(lambda x: 'id: {} | size: {}'.format(x['hier_id'], x['size'])))
    plt.xticks(
        x_labels,
        x_label_text,
        rotation='vertical'
        )
    plt.ylabel('Rumor')
    plt.yticks(np.arange(len(rumor_labels)) + 0.5, rumor_labels)
    for tic in ax.yaxis.get_major_ticks():
        tic.tick1On = tic.tick2On = False
    cb = plt.colorbar()
    label_text = 'Rumor Tweet Count'
    if logscale:
        label_text += '\n(log10 scale)'
    cb.set_label(label_text)
    plt.tight_layout()
    plt.show()

    # Save the output
    if not output.endswith('.pdf'):
        output = output+'.pdf'
    fig.savefig(output, format='pdf')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Visualizes NNGH Accuracy Results')
    parser.add_argument(
        'model_path', help='Path to the SFrame',
        type=str)
    parser.add_argument(
        'output', help='The output path',
        type=str)
    parser.add_argument(
        '-r', '--radius', help='The radius for which to filter the model cache.',
        type=float, default=3.0)
    parser.add_argument(
        '-c', '--cutoff', help='The minimum number of rumor tweets which must be included in a component for it to appear in the visual.',
        type=int, default=None)
    parser.add_argument(
        '-l', '--logscale', help='Whether or not to use a log scale for color intensity',
        action='store_true')
    parser.add_argument(
        '-w', '--width_by_size', help='Whether or not to adjust the width of each column by the component size',
        action='store_true')
    parser.add_argument(
        '-u', '--unrealted', help='Whether or not to include a column for unrealted tweets',
        action='store_true')

    args = parser.parse_args()
    main(args.model_path, args.output, args.radius, cutoff=args.cutoff, logscale=args.logscale, width_by_size=args.width_by_size, include_unrelated=args.unrealted)
    exit()
