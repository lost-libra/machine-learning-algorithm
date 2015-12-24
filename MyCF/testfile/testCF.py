#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import os

def CollaborativeFiltering(srcPath):
	testData = pd.read_csv(srcPath, header = 0, index_col = 0)

	# Cause the type of columns that read in csv is str, we need to convert it into int
	int_col = []
	for col in testData.columns:
		icol = int(col)
		int_col.append(icol)
	testData.columns = int_col

	predicted_data = testData.copy()

	print "Computing the correlation, please wait......"
	corr = predicted_data.T.corr(min_periods=1)
	corr_clean = corr.dropna(how='all')					#drop nan data by index
	corr_clean = corr_clean.dropna(axis=1, how='all')	#drop nan data by column

	predicted_data = predicted_data.loc[corr_clean.index]

	print "Predicting the unrated movies, please wait......"
	for user in corr_clean.index.values:
		noRating = testData.ix[user]
		noRating = noRating[noRating.isnull()]			#movies that user never rated before
		corr_user = corr_clean[user].drop(user)			#drop user itself
		corr_user = corr_user[corr_user>0.1].dropna()	#pick corr_user that the correlation>0.1
		for movie in noRating.index:
			prediction = []
			for other in corr_user.index:
				if not np.isnan(testData.ix[other, movie]):
					prediction.append((testData.ix[other, movie], corr_clean[user][other]))
			if prediction:
				predicted_data[movie][user] = sum([value*weight for value, weight in prediction])/sum([pair[1] for pair in prediction])

	print "Writing predicted data into csv file, please wait......"
	predicted_data.to_csv('pretestDatacv_3.csv')

	print "Done, please check your pretestData.csv"
	return predicted_data
	
def main():
	localPath = os.getcwd()
	srcPath = os.path.join(localPath, 'datatestcv_3.csv')
	print 'srcPath = ', srcPath
	predicted_data = CollaborativeFiltering(srcPath)
	print predicted_data[:10]

if __name__ == '__main__':
		main()	