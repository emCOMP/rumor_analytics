import datetime
from matplotlib import pyplot as plt
from matplotlib.colors import ColorConverter
import graphlab as gl
import graphlab.aggregate as agg
import argparse


class CoverageExplorer(object):

    def __counts_over_time__(
            self, sf, id_col='mongo_id', time_col='created_ts',
            datetime_format='%Y-%m-%d %H:%M:%S', event_csv=False):
        print '\nCalculating counts per minute...'
        # Convert from string to datetime.
        sf[time_col] = sf[time_col].apply(
            lambda x: datetime.datetime.strptime(x, datetime_format))
        # Find the earliest tweet.
        if event_csv:
            self.start = sf[time_col].min()
        # Add a new column with minutes from collection start.
        sf[self.chunk_name] = sf[time_col].apply(
            lambda x: int((x - self.start).total_seconds()) / 60)
        if event_csv:
            self.start_min = sf[self.chunk_name].min()
            self.end_min = sf[self.chunk_name].max()

        # Fill in any minutes we don't have tweets for with 0s
        # FIX ME (Is this even needed?)
        '''
        tmp = gl.SFrame()
        tmp.add_column(
            gl.SArray.from_sequence(self.start_min, self.end_min + 1),
            self.chunk_name
            )
        sf = tmp.join(sf, on=self.chunk_name, how='left')
        sf.fillna(self.chunk_name, 0)
        '''

        # Calculate the counts per unique timestamp
        counts = sf.groupby(
            self.chunk_name, {self.count_name: agg.COUNT(id_col)}
        ).sort(self.chunk_name)

        if event_csv:
            self.event_rows = counts[[self.chunk_name]]

        else:
            counts = self.event_rows.join(
                counts, on=self.chunk_name, how='left')
            counts = counts.fillna(self.count_name, 0)

        return counts

    def __user_select_column__(self, message, col_names):
        done = False
        val = None
        while not done:
            print '\n\n', message
            col_list = [str(i) + '. ' + str(v)
                        for i, v in enumerate(col_names)]
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
        sf = gl.SFrame.read_csv(csv_path, header=True, verbose=False)

        # Query the user for which columns are which.
        id_col_name = self.__user_select_column__(
            message='Which column contains the database id?',
            col_names=sf.column_names())
        time_col_name = self.__user_select_column__(
            message='Which column contains the time of creation?',
            col_names=sf.column_names())

        return self.__counts_over_time__(
            sf, id_col=id_col_name,
            time_col=time_col_name, event_csv=event_csv)

    def __init__(
            self,
            event_name,
            event_csv,
            colors,
            time_chunk_name='minutes',
            count_name='tweet_count'):

        # Set label parameters.
        self.event_name = event_name
        self.chunk_name = time_chunk_name
        self.count_name = count_name

        #Convert Colors to MPL format
        cv = ColorConverter()
        self.event_color = cv.to_rgba(colors[0])
        self.rumor_color = cv.to_rgba(colors[1])

        # Process the event CSV.
        self.event_counts = self.csv_to_counts(event_csv, event_csv=True)
        self.event_y = list(self.event_counts[self.count_name])
        self.event_x = range(self.event_counts.num_rows())

    def generate_comparison(self, rumor_csv_path):
        # rumor_path = raw_input('Path to rumor csv: ')
        f_name = raw_input('Output file name: ')
        print 'Rendering...'
        # Process rumor CSV.
        rumor_counts = self.csv_to_counts(rumor_csv_path)
        rumor_x = range(rumor_counts.num_rows())
        rumor_y = list(rumor_counts[self.count_name])

        # Create figure
        fig, ax = plt.subplots()

        # Plot event data
        ax.bar(self.event_x, self.event_y, color=self.event_color,
               fc=self.event_color, ec=self.event_color)

        # Plot rumor data
        ax.bar(rumor_x, rumor_y, color=self.rumor_color,
               fc=self.rumor_color, ec=self.rumor_color)

        # Set the y axis range
        rumor_max = rumor_counts[self.count_name].max()
        ax.set_ylim([0, int(rumor_max * 1.2)])

        # Add title, label axes
        plt.title(str(self.event_name) + ' Coverage')
        plt.ylabel(self.count_name)
        plt.xlabel(self.chunk_name)

        print 'Saving...'
        plt.savefig(f_name + '.pdf', format='pdf')
        print 'Complete!'


def main(args):
    ce = CoverageExplorer(
        args.event_name, args.event_csv,
        colors=[args.event_color, args.rumor_color])

    ce.generate_comparison(args.rumor_csv)
    exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Compares tweet collection coverage for an event and \
                    a rumor, and outputs a graph of the comparison.')
    parser.add_argument(
        'event_name', help='name of the crisis event', type=str)
    parser.add_argument(
        'event_csv', help='path to a csv dump of the whole event', type=str)
    parser.add_argument(
        'rumor_csv', help='path to a csv dump of the rumor tweets', type=str)
    parser.add_argument(
        '-ec', '--event_color', help='color to use for event capture volume',
        type=str, required=False, default='black')
    parser.add_argument(
        '-rc', '--rumor_color', help='color to use for rumor capture volume',
        type=str, required=False, default='red')
    args = parser.parse_args()
    main(args)
