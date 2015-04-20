import numpy as np
from progressbar import ProgressBar
from scipy.sparse import csr_matrix

row_count = 0
feature_count = 0
with open('matrix.txt','rb') as f:
	row_count = sum(1 for i in f)

with open('feature_names.txt','rb') as f:
	feature_count = sum(1 for i in f)

with open('matrix.txt','rb') as f:
	pb = ProgressBar(maxval=row_count+1).start()
	row = 0
	m = csr_matrix((row_count,feature_count), dtype=np.bool_)

	for line in f:
		l = line.strip().split(',')
		if l[0]:
			l = map(int,l)
			row_count, col_count = m.shape

			#If the matrix is out of space, resize it.
			if row >= row_count:
				new_rows = row_count + 10
				m.reshape((new_rows, col_count))
				#self.row_resize_step *= 1.5
			
			if  max(l) >= col_count:
				new_cols = max(l)+1
				m.reshape((row_count, new_cols))
				#self.col_resize_step *= 1.5
			
			for col in l:
				try:
					m[row,col] = True
				except:
					new_cols = col+1
					m.reshape((row_count, new_cols))
					m[row,col] = True

		pb.update(row)
		row += 1

	pb.finish()

with open('feature_matrix_csr', 'wb') as backup:
	np.save(backup, m)

with open('feature_matrix_csr_log.txt', 'wb') as status_log:
	status_log.write('Great Success!')

