#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib
import numpy as np
import os
import pandas as pd
from sklearn.cluster.bicluster import ChengChurch

def main():
	local_path = os.getcwd()
	src_name = 'pretestData.csv'
	src_path = os.path.join(local_path, src_name)
	pd_data = pd.read_csv(src_path, header = 0, index_col = 0)
	int_col = [int(x) for x in pd_data.columns.values]
	pd_data.columns = int_col
	data = (pd_data.values) * 100
	print data.shape, type(data)

	k = 4
	model = ChengChurch(n_clusters=k, max_msr=100, deletion_threshold=1.1, inverse_rows=True, random_state=0)
	model.fit(data)

	nau = np.array([])
	nam = np.array([])
	for i in range(k):
		print model.get_indices(i)
		print model.get_shape(i)
		nau = np.append(nau, model.get_indices(i)[0])
		nam = np.append(nam, model.get_indices(i)[1])
	print 'user number of clustered = ', len(set(nau)), 'movie number of clustered = ', len(set(nam))


if __name__ == '__main__':
	main()