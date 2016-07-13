import matplotlib as mpl
mpl.use('AGG')
from matplotlib import pyplot as plt
from nngh import NNGraphHierarchy
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import graphlab as gl
gl.set_runtime_config('GRAPHLAB_DEFAULT_NUM_PYLAMBDA_WORKERS', 32)
import graphlab.numpy
import graphlab.aggregate as agg


def __old_component_distances(m, component_ids):
    g = m.g
    filtered_verts = g.vertices.filter_by(component_ids, 'hier_id')
    nodes = filtered_verts[['__id','hier_id']]
    edges = g.edges.join(nodes, on={'__src_id':'__id'}, how='right')
    within_component_distance = edges.groupby('hier_id', {'within_average_distance': agg.MEAN('distance')})
    tweet_distances = edges.groupby('__src_id', {'average_distance': agg.MEAN('distance')})
    representative_ids = tweet_distances.join(nodes, on={'__src_id':'__id'}, how='left').groupby('hier_id', {'__src_id': agg.ARGMIN('average_distance', '__src_id')})
    representatives = filtered_verts.filter_by(representative_ids['__src_id'], '__id')
    knn = gl.nearest_neighbors.create(representatives, label='__id', distance=m.settings['distance'])
    pairwise_rep_distances = knn.query(representatives, label='__id', radius=m.settings['cache_radius'])
    between_component_distances = pairwise_rep_distances.groupby('query_label', {'between_average_distance': agg.MEAN('distance')})
    between_component_distances = between_component_distances.join(nodes, on={'query_label':'__id'}, how='left')
    del between_component_distances['query_label']
    result = within_component_distance.join(between_component_distances, on='hier_id', how='outer')
    result['between_within_ratio'] = result.apply(lambda x: x['between_average_distance'] / x['within_average_distance'])
    return result

def component_distances(m, component_ids):
    g = m.g
    # Make a graph with just the components in 'component_ids'
    filtered_verts = g.vertices.filter_by(component_ids, 'hier_id')
    nodes = filtered_verts[['__id','hier_id']]
    edges = g.edges.join(nodes, on={'__src_id':'__id'}, how='right')

    # Calculate the average distance between tweets within each component
    within_component_distance = edges.groupby('hier_id', {'within_average_distance': agg.MEAN('distance')})
    all_distances = m.cache.join(nodes, on={'__src_id':'__id'}, how='right')

    # Get the distances between the points in each component and
    # points in OTHER components only.
    between_component_distances = None
    for c in component_ids:
        component_nodes = nodes.filter_by([c], 'hier_id', exclude=False)['__id']
        distances = all_distances.filter_by(component_nodes ,'__src_id', exclude=False).filter_by(component_nodes ,'__dst_id', exclude=True)
        top_neighbors = distances.groupby('__src_id', {'nearest_external_neighbor': agg.MIN('distance')})
        top_neighbors = nodes.join(top_neighbors, on={'__id':'__src_id'}, how='right')
        if not between_component_distances:
            between_component_distances = top_neighbors
        else:
            between_component_distances = between_component_distances.append(top_neighbors)
    between_collapsed = between_component_distances.groupby('hier_id', {'nearest_external_neighbor': agg.MIN('nearest_external_neighbor')})
    return within_component_distance.join(between_collapsed, on='hier_id', how='outer')

def rumor_distances(m):
    g = m.g
    # Make a graph with just the components in 'component_ids'
    nodes = m.g.vertices[['__id','rumor','hier_id']]
    edges = g.edges.join(nodes, on={'__src_id':'__id'}, how='right')
    edges = edges.join(nodes, on={'__dst_id':'__id'}, how='right')
    edges.rename({'rumor':'src_rumor', 'rumor.1':'dst_rumor'})

    # Calculate the average distance between tweets within each component
    distance_by_rumor = edges.groupby(['src_rumor','dst_rumor'], {'average_distance': agg.MEAN('distance'), 'std': agg.STD('distance'), 'distance_quantiles': agg.QUANTILE('distance', [0.05, 0.25, 0.50, 0.75, 0.95])})
    distance_by_rumor = distance_by_rumor[['src_rumor', 'dst_rumor', 'average_distance', 'std', 'distance_quantiles']].unpack('distance_quantiles', column_name_prefix='').sort(['src_rumor', 'average_distance'])
    distance_by_rumor.rename({'0':'5th Percentile', '1':'25th Percentile', '2':'50th Percentile', '3':'75th Percentile', '4':'95th Percentile'})
    return distance_by_rumor

def neighbors_by_rumor(m):
    g = m.g

    # Make a graph with just the components in 'component_ids'
    nodes = m.g.vertices[['__id','rumor','hier_id']]
    edges = g.edges[g.edges['__src_id'] != g.edges['__dst_id']].join(nodes, on={'__src_id':'__id'}, how='right')
    edges = edges.join(nodes, on={'__dst_id':'__id'}, how='left')
    edges.rename({'rumor':'src_rumor', 'rumor.1':'dst_rumor'})
    edges, isolates = edges.dropna_split('dst_rumor')
    isolates = isolates.groupby('src_rumor', {'number_of_isolates': agg.COUNT_DISTINCT('__src_id')})
    # Find the nearest tweet to each tweet and record its rumor and how far away it is.
    neighbor_rumors = edges.groupby('__src_id', {'nearest_rumor': agg.ARGMIN('distance', 'dst_rumor'), 'nearest_neighbor_distance': agg.MIN('distance')})
    result = neighbor_rumors.join(nodes, on={'__src_id':'__id'}, how='left')
    result.rename({'rumor':'src_rumor'})
    result = result.groupby('src_rumor', {'nearest_rumors':agg.FREQ_COUNT('nearest_rumor'), 'average_nearest_distance': agg.MEAN('nearest_neighbor_distance'), 'total_tweets':agg.COUNT()})
    result['nearest_neighbor_percentages'] = result.apply(lambda x: {k : (float(v) / x['total_tweets']) for k,v in x['nearest_rumors'].iteritems()} if x['nearest_rumors'] else {'ISOLATE':1} )
    result = result.join(isolates, on='src_rumor', how='outer')
    result['percentage_isolates'] = result.apply(lambda x:  x['total_tweets'] / (float(x['number_of_isolates']) + x['total_tweets']))
    return result

def main(path, output, radius, cutoff=None, logscale=False, width_by_size=False, include_unrelated=False, hmax=100, hmin=0, micro_size=3, dump_components=True, dump_micros=False):
    arg_dict = locals()
    m = NNGraphHierarchy(path)
    if m.settings['radius'] != radius:
        m.g = m.get_graph(radius)
        m.settings['radius'] = radius
        m.save(path)
    g = m.g
    sf = g.vertices
    sf['rumor'] = sf['rumor'].fillna('None')
    rumors = list(sf['rumor'].unique())
    groups = sf.groupby(['hier_id', 'rumor'], {'tweets': agg.COUNT()})
    data = groups.unstack(['rumor', 'tweets'], 'rumor_tweets').unpack('rumor_tweets', limit=rumors, column_types=[int for r in rumors], column_name_prefix='')
    # Compute the size of each component
    data['size'] = data[rumors].apply(lambda x: sum([v for k,v in x.iteritems() if v]))
    # data = gl.SFrame('tmp.sf')
    data['hier_id'] = data['hier_id'].apply(str)
    # rumors = ["suicide", "hadley", "None", "flag", "lakemba", "airspace"]
    rumors = list(sf['rumor'].unique())
    if logscale:
        data['log_size'] = data['size'].clip_lower(1).apply(np.log10).fillna(0)
    data['rumor_tweets'] = data[[r for r in rumors if r != 'None']].apply(lambda x: sum([v for k,v in x.iteritems() if v]))
    rumor_only = data.dropna([r for r in rumors if r != 'None'], how='all')
    isolates = rumor_only[rumor_only['size'] <= micro_size]
    
    # Add an aggregated component for isolates.
    tmp = gl.SFrame({'hier_id': ['micro_components']})
    extras = ['rumor_tweets', 'size']
    if logscale:
        extras.append('log_size')
    for r in rumors + extras:
        tmp[r] = [isolates[r].sum()]
    rumor_only = rumor_only.append(tmp)
    
    # Filter based on the cutoff if one was provided.
    if cutoff:
        # Aggregate all of the components we're going to exclude.
        tmp = gl.SFrame({'hier_id': ['excluded']})
        excluded = rumor_only[rumor_only['rumor_tweets'] < cutoff]
        for r in rumors + extras:
            tmp[r] = [excluded[r].sum()]
        try:
            rumor_only = rumor_only[rumor_only['rumor_tweets'] >= cutoff].append(tmp)
        except RuntimeError:
            for c, t1, t2 in zip(rumor_only.column_names(), rumor_only.column_types(), tmp.column_types()):
                if t1 != t2:
                    rumor_only[c] = rumor_only[c].apply(t2)
            rumor_only = rumor_only[rumor_only['rumor_tweets'] >= cutoff].append(tmp)
    
    for r in rumors:
        data[r] = data[r].fillna(0)
        if logscale:
            data[r] = data[r].clip_lower(1).apply(np.log10).fillna(0)
        
        if r in rumor_only.column_names():
            rumor_only[r] = rumor_only[r].fillna(0)
            if logscale:
                rumor_only[r] = rumor_only[r].clip_lower(1).apply(np.log10).fillna(0)

    rumors.remove('None')
    if include_unrelated:
        # We remove it and add it back in to ensure it is the last column.
        rumors.append('None')

    rumor_component_tweets = m.get_components(list(rumor_only['hier_id'].unique().apply(lambda x: int(x) if x.isdigit() else -1)), component_label='hier_id')

    if dump_components:
        out = rumor_component_tweets[['tweet_id', 'orig_text', 'hier_id', 'rumor', 'time']].sort(['hier_id', 'rumor', 'time'], False)
        out.save('{}.tweet_text.csv'.format(output.replace('.pdf','')))
        del out

    if dump_micros:
        out = m.get_components(list(isolates['hier_id'].unique().apply(lambda x: int(x) if x.isdigit() else -1)), component_label='hier_id')
        out = out[['tweet_id', 'orig_text', 'hier_id', 'rumor', 'time']].sort(['hier_id', 'rumor', 'time'], False)
        out.save('{}.micro_tweet_text.csv'.format(output.replace('.pdf','')))
        del out

    # Find average component distance
    component_dists = component_distances(m, list(rumor_only['hier_id'].unique().apply(lambda x: int(x) if x.isdigit() else -1)))
    component_dists.save('{}.component_dists.csv'.format(output.replace('.pdf','')))
    rumor_dists = rumor_distances(m)
    rumor_dists.save('{}.rumor_dists.csv'.format(output.replace('.pdf','')))
    rumor_neighbors = neighbors_by_rumor(m)
    rumor_neighbors.save('{}.rumor_neighbors.csv'.format(output.replace('.pdf','')))
    tmp = rumor_only[rumors]
    rumor_labels = [c for c in tmp.column_names() if c in rumors]
    z = gl.numpy.array(rumor_only[rumors].sort(rumors)).T
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

    # Prepare the output.
    if not output.endswith('.pdf'):
        output = output+'.pdf'
    
    with PdfPages(output) as pdf:
        # Plot the heatmap
        fig = plt.figure()
        ax = fig.add_subplot(111)
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
        pdf.savefig()
        plt.close()

        # # Plot the cluster tightness.
        # fig = plt.figure()
        # ax = fig.add_subplot(111)
        # plt.bar(h[1][:-1][mask], h[0][mask])
        # plt.title('Component Size Distribution')
        # plt.xlabel('Component Size\n(# of tweets)')
        # plt.ylabel('Frequency \n(# of components)')
        # pdf.savefig()
        # plt.close()

        # Setup histogram data.
        hist_data = gl.numpy.array(data['size'])
        h = np.histogram(hist_data, bins=np.arange(hist_data.min(), hist_data.max(), (hist_data.max() - hist_data.min()) / 20))
        mask = (h[1][:-1] <= np.percentile(h[1][:-1], hmax)) * (h[1][:-1] >= np.percentile(h[1][:-1], hmin))
        
        # Plot the histogram.
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.bar(h[1][:-1][mask], h[0][mask])
        plt.title('Component Size Distribution')
        plt.xlabel('Component Size\n(# of tweets)')
        plt.ylabel('Frequency \n(# of components)')
        pdf.savefig()
        plt.close()

        fig = plt.figure(facecolor='white')
        ax = fig.add_subplot(111)
        ax.text(0.05, 0.95, "Report Parameters", horizontalalignment='left',verticalalignment='center',transform=ax.transAxes, fontsize=14, fontweight='bold')
        ax.text(0.05, 0.7,'\n'.join(["{}: {}".format(k, v) for k,v in arg_dict.iteritems()]), horizontalalignment='left',verticalalignment='center',transform=ax.transAxes)
        plt.axis('off')
        pdf.savefig()
        plt.close()

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
    parser.add_argument(
        '-hmax', '--hist_max', help='The maximum percentile to plot on the component size histogram',
        type=int, default=100)
    parser.add_argument(
        '-hmin', '--hist_min', help='The minimum percentile to plot on the component size histogram',
        type=int, default=0)
    parser.add_argument(
        '-m', '--micro_size', help='The the maximum size for a component to be considered a micro-component',
        type=int, default=3)
    parser.add_argument(
        '-dc', '--dump_components', help='Whether or not to dump component tweet texts',
        action='store_true', default=True)
    parser.add_argument(
        '-dm', '--dump_micros', help='Whether or not to dump micro-component tweet texts',
        action='store_true', default=False)

    args = parser.parse_args()
    main(args.model_path, args.output, args.radius, cutoff=args.cutoff, logscale=args.logscale, width_by_size=args.width_by_size, include_unrelated=args.unrealted, hmax=args.hist_max, hmin=args.hist_min, micro_size=args.micro_size, dump_components=args.dump_components, dump_micros=args.dump_micros)
    exit()
