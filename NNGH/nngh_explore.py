import graphlab as gl
from explore import Explorer

sf = gl.load_sframe('z1')
sf.groupby('hier_id', operations={'term_totals': agg.SUM('bow')})