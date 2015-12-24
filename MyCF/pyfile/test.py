#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import os

def test():
	localPath = os.getcwd()
	srcPath = os.path.join(localPath, '../src/ratings.csv')
	print 'srcPath = ', srcPath

	columns = ['userID', 'movieID', 'rating', 'timestamp']
	ratings = pd.read_csv(srcPath, header = 1, names = columns)
	data = ratings.pivot(index = 'userID', columns = 'movieID', values = 'rating')
	print data.columns
	print 'data = ', data.loc[:5, data.columns]

def main():
	localPath = os.getcwd()
	srcPath = os.path.join(localPath, 'src/ratings.csv')
	print 'srcPath = ', srcPath

	columns = ['userID', 'movieID', 'rating', 'timestamp']
	ratings = pd.read_csv(srcPath, header = 1, names = columns)
	print 'ratings = ', ratings[:3]

	movieNum = ratings['movieID'].nunique()
	movieID = ratings['movieID'].unique()
	userNum = ratings['userID'].nunique()
	print 'movieID = ', ratings['movieID'].unique(), ', len(movieID) = ', movieNum
	print 'len(userNum) = ', userNum

	data = ratings.pivot(index = 'userID', columns = 'movieID', values = 'rating')
	print 'data = ', data[:5]

	userWatchNum = pd.Series(index = data.index)
	for i in data.index:
		userWatchNum[i] = data.ix[i].dropna().count()
	userWatchNum.order(ascending = False, inplace = True)
	print 'Biggest watched time = ', userWatchNum.head(10), '\nSmallest watched time = ', userWatchNum.tail(10)

	print 'The both watched movie number = ', data.ix[userWatchNum.index.values[0]][data.ix[userWatchNum.index.values[1]].notnull()].dropna().count()
	print 'The corr = ', data.ix[(userWatchNum.index.values[0])].corr(data.ix[(userWatchNum.index.values[1])])

	corr = data.T.corr(min_periods=200)
	corr_clean = corr.dropna(how='all')					#drop nan data by index
	corr_clean = corr_clean.dropna(axis=1, how='all')	#drop nan data by column

	lucky = np.random.permutation(corr_clean.index)[0]	#permutate the corr_clean's index and choice the first one to analyze
	print lucky
	gift = data.ix[lucky]
	gift = gift[gift.isnull()]
	corr_lucky = corr_clean[lucky].drop(lucky)
	corr_lucky = corr_lucky[corr_lucky>0.1].dropna()
	for movie in gift.index:
		prediction = []
		for other in corr_lucky.index:
			if not np.isnan(data.ix[other, movie]):
				prediction.append((data.ix[other, movie], corr_clean[lucky][other]))
		if prediction:
			gift[movie] = sum([value*weight for value, weight in prediction])/sum([pair[1] for pair in prediction])
	print gift.dropna().order(ascending = False)


if __name__ == '__main__':
		test()	