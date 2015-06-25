import datetime
from matplotlib import pyplot as plt
import graphlab as gl
import graphlab.aggregate as agg
import argparse

class CoverageExplorer(object):

    def __counts_over_time__(
        self, sf, id_col='mongo_id', time_col='created_ts',
        datetime_format='%Y-%m-%d %H:%M:%S', event_csv=False):
        # Convert from string to datetime.
        sf[time_col] = sf[time_col].apply(lambda x: datetime.datetime.strptime(x, datetime_format))
        # Find the earliest tweet.
        start = sf[time_col].min()
        # Add a new column with minutes from collection start.
        sf[self.chunk_name] = sf[time_col].apply(lambda x: int((x - start).total_seconds())/60)
        # Calculate the counts per unique timestamp
        counts = sf.groupby(self.chunk_name,{self.count_name:agg.COUNT(id_col)}).sort(self.chunk_name)
        
        if event_csv:
            self.event_rows = sf[[self.chunk_name]]
        else:
            counts = self.event_rows.join(counts, on=self.chunk_name, how='left')
            counts = counts.fillna(self.count_name, 0)

        return counts

    def __user_select_column__(self, message, col_names):
        done = False
        val = None
        while not done:
            print '\n\n', message
            col_list = [str(i)+'. '+str(v) for i,v in enumerate(col_names)]
            for i in col_list:
                print i
            usr_input = raw_input('Please enter a number:')
            try:
                usr_input = int(usr_input)
                if usr_input >= 0 and usr_input < len(col_list):
                    val = col_names[usr_input]
                    done = True
                    break
                else:
                    continue
            except:
                continue

        return val

    def csv_to_counts(self, csv_path, event_csv=False):
        sf = gl.SFrame.read_csv(csv_path, header=True)
        id_col_name = self.__user_select_column__(
            message='Which column contains the database id?',
            col_names=sf.column_names())
        time_col_name = self.__user_select_column__(
            message='Which column contains the time of creation?',
            col_names=sf.column_names())

        return self.__counts_over_time__(sf, id_col=id_col_name, time_col=time_col_name, event_csv=event_csv)


    def __init__(self, event_name, event_csv, time_chunk_name='minutes', count_name='tweet_count'):
        
        # Set label parameters.
        self.event_name = event_name
        self.chunk_name = time_chunk_name
        self.count_name = count_name

        # Process the event CSV.
        self.event_counts = self.csv_to_counts(event_csv, event_csv=True)
        self.event_y = list(self.event_counts[self.count_name])
        self.event_x = self.event_counts.num_rows()


    def generate_comparison(self, rumor_csv_path):
        #rumor_path = raw_input('Path to rumor csv: ')
        f_name = raw_input('Output file name: ')

        # Process rumor CSV.
        rumor_counts = self.csv_to_counts(rumor_csv_path)
        rumor_x = rumor_counts.num_rows()
        rumor_y = list(rumor_counts[self.count_name])
        fig, ax = plt.subplots()
        ax.bar(self.event_x, self.event_y)
        ax.bar(rumor_x, rumor_y, color=[1,0,0], fc=[1,0,0], ec=[1,0,0])
        plt.ylabel(self.count_name)
        plt.xlabel(self.chunk_name)
        plt.title(str(event_name)+' Coverage')
        plt.savefig(f_name, format='pdf')
        print 'Saving Complete!'

def main(args):
    ce = CoverageExplorer(args.event_name, args.event_csv)
    ce.generate_comparison(args.rumor_csv)
    exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('event_name', help='name of the crisis event', type=str)
    parser.add_argument('event_csv', help='a path to a csv dump of the whole event', type=str)
    parser.add_argument('rumor_csv', help='a path to a csv dump of the rumor tweets', type=str)
    args = parser.parse_args()
    main(args)

