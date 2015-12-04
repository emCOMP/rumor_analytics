import graphlab as gl
from graphlab.toolkits.recommender.util import precision_recall_by_user
from nngh import NNGraphHierarchy

# The columns we will use for this script (we'll drop all the other columns for simplicity)
columns = ['mongo_id', 'text', 'hier_id','rumor']

def main():
    # Load in our original dataset.
    original_data = gl.SFrame('data/sydney_doc_vecs').select_columns(['mongo_id', 'text', 'rumor'])

    # Load in the models run at each quantile point.
    result_path = 'output/pr/q'
    result_quantiles = ['05', '25', '50', '75', '95']
    models = []
    for q in result_quantiles:
        models.append( (NNGraphHierarchy(result_path+q), int(q)) )

    # Load in the top 5 retweeted tweets for each rumor.
    trt = gl.SFrame.read_csv('data/top_rts.csv')

    rumors = ['hadley', 'airspace', 'flag', 'lakemba', 'suicide']
    # For each rumor compute a percision recall curve
    for r in rumors:
        print r
        # Get all of the tweets for a given rumor (the 'correct' case answer).
        test_data = original_data.filter_by([r], 'rumor')

        # Create an SFrame in the User-Reccomendation format using those tweets.
        test_data = gl.SFrame({'User':trt[r],'rumor':gl.SArray.from_const(r, trt.num_rows())}).join(test_data, on='rumor', how='left')
        del test_data['rumor']
        del test_data['text']
        test_data.rename({'mongo_id':'Item'})
        print test_data

        # Get the model's results using the top 5 retweeted tweets as the query tweets.
        query_results = None
        for m, q in models:
            tmp = m.query(trt[r], label='mongo_id', component_label='hier_id')
            tmp['quantile'] = gl.SArray.from_const(q, tmp.num_rows())

            if not query_results:
                query_results = tmp
            else:
                query_results = query_results.append(tmp)

        # (NNGH returns an extra column called 'hier_id' which isn't returned
        # by most GraphLab queries, so we'll delete it to put our SFrame
        # in the right format.
        del query_results['hier_id']
        query_results.rename({'query_id':'User', 'reference_id':'Item', 'quantile':'Rank'})
        print query_results.head()

        # Compute the PR curve and save it.
        pr = precision_recall_by_user(test_data, query_results, [i[1] for i in models])
        pr.save('results/pr.{}.nngh.csv'.format(r))



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Generates percsion-recall curves for each rumor for the given NNGH model results')
    main()
    exit()
