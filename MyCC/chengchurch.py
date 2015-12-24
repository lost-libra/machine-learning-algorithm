import urllib
import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas.tools.plotting import parallel_coordinates
import matplotlib.pylab as plt
from sklearn.cluster.bicluster import ChengChurch

'''
# get data
url = "http://arep.med.harvard.edu/biclustering/lymphoma.matrix"
lines = urllib.urlopen(url).read().strip().split('\n')
# insert a space before all negative signs
lines = list(' -'.join(line.split('-')).split(' ') for line in lines)
lines = list(list(int(i) for i in line if i) for line in lines)
data = np.array(lines)
pd_data = pd.DataFrame(data)
pd_data.to_csv('lymphoma.csv')
'''

pd_data = pd.read_csv('lymphoma.csv', header = 0, index_col = 0)
data = pd_data.values
print type(data), data.shape
# replace missing values, just as in the paper
generator = np.random.RandomState(0)
idx = np.where(data == 999)
data[idx] = generator.randint(-800, 801, len(idx[0]))

# cluster with same parameters as original paper
model = ChengChurch(n_clusters=100, max_msr=1200,
                    deletion_threshold=1.2, inverse_rows=True,
                    random_state=0)
model.fit(data)

# find bicluster with smallest msr and plot it
msr = lambda a: (np.power(a - a.mean(axis=1, keepdims=True) -
                          a.mean(axis=0) + a.mean(), 2).mean())
msrs = list(msr(model.get_submatrix(i, data)) for i in range(100))
arr = model.get_submatrix(np.argmin(msrs), data)
print type(arr), arr.shape
df = DataFrame(arr)
df['row'] = map(str, range(arr.shape[0]))
parallel_coordinates(df, 'row', linewidth=1.5)
plt.xlabel('column')
plt.ylabel('expression level')
plt.gca().legend_ = None
plt.show()