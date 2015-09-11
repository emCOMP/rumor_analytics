import graphlab as gl
import graphlab.aggregate as agg
import itertools


def rumor_component_distribution(sf, related, component_col='hier_id'):
    print 'Calculating Accuracy...'
    rumors = related['rumor'].unique()

    # Will hold SFrames of related tweets for each rumor.
    # {'Rumor_Name': SFrame}
    rt = {}

    # Create an SFrame for each rumor containing the related tweets.
    for r in rumors:
        rt[r] = related.filter_by([r], 'rumor')['mongo_id']

    # Get one copy of the hier_id name for every member of that hier_component.
    # tmp = [[r['hier_id'] for i in r['members']] for r in membership]
    # hier_ids = [i for i in itertools.chain.from_iterable(tmp)]
    # # Get a concatenated list of all the components.
    # members = [i for i in itertools.chain.from_iterable(membership['members'])]

    # # Make an SFrame containing every component, and the id of
    # # its parent hier_component.
    # comp_memberships = gl.SFrame(
    #     {'hier_id': hier_ids, 'component_id': members})

    # # Get the size of each low-level component.
    # comp_sizes = sf.groupby('component_id', operations={'tweets': agg.COUNT()})

    # # Join the hier_ids onto the component sizes.
    # comp_sizes = comp_sizes.join(
    #     comp_memberships, on='component_id', how='outer')

    # # Sum all of the component_sizes over the ids.
    # final_result = comp_sizes.groupby(
    #     'hier_id', operations={'tweets': agg.SUM('tweets')})
    final_result = sf.groupby('hier_id', operations={'tweets': agg.COUNT()})

    for k, v in rt.iteritems():
        results = sf.filter_by(v, 'mongo_id')
        rel_counts = results.groupby(
            component_col, operations={k: agg.COUNT()})

        final_result = final_result.join(rel_counts, on='hier_id', how='outer')

    final_result.rename({'hier_id': 'component', 'tweets': 'size'})
    for col in final_result.column_names():
        final_result[col] = final_result[col].fillna(0)
        final_result = final_result.sort(col, False)

    print 'Final Accruacy Report:\n'
    print final_result
    return final_result


def top_level_report(sf, top_n=10):
    # Find all unique hier_ids and make a list of their respective
    # child component_ids.
    hier_sf = sf[['component_id', 'hier_id']].groupby(
                'hier_id', {'children': agg.CONCAT('component_id')})
    # Add a column with the size of the top-level components.
    hier_size = hier_sf.groupby(
                    'hier_id', operations={'size': agg.COUNT()})
    hier_sf = hier_sf.join(hier_size, on='hier_id', how='left')

    # Find the top bigrams for each hier id.
    top_bigrams = {'top_bigrams': []}
    top_bigrams['hier_id'] = []

    for h in hier_sf:
        top_bigrams['hier_id'].append(h['hier_id'])

        # Get only the rows belonging to this hier_id:
        cur_sf = sf[sf['hier_id'] == h['hier_id']]
        terms = {}
        for r in cur_sf['bigrams']:
            for t in r:
                terms[t] = terms.get(t, 0) + r[t]
        terms = [(k, v) for k, v in terms.iteritems()]
        ranked = sorted(terms, reverse=True, key=lambda x: x[1])
        top = [{t: count} for t, count in ranked[:top_n]]
        top_bigrams['top_bigrams'].append(top)

    top_bigrams = gl.SFrame(top_bigrams)
    hier_sf = hier_sf.join(top_bigrams, on='hier_id')

    return hier_sf


if __name__ == '__main__':
    sf = gl.load_sframe('radius_tests/z1')
    mem = gl.load_sframe('radius_tests/z1_membership')
    rel = gl.SFrame.read_csv('sydney_rumors.csv')
    rumor_component_distribution(sf, rel, mem)
