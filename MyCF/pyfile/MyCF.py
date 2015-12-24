#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import os

def CollaborativeFiltering(srcPath):
	columns = ['userID', 'movieID', 'rating', 'timestamp']
	ratings = pd.read_csv(srcPath, header = 1, names = columns)

	data = ratings.pivot(index = 'userID', columns = 'movieID', values = 'rating')
	predicted_data = data.copy()

	print "Computing the correlation, please wait......"
	corr = data.T.corr(min_periods=200)
	corr_clean = corr.dropna(how='all')					#drop nan data by index
	corr_clean = corr_clean.dropna(axis=1, how='all')	#drop nan data by column

	predicted_data = predicted_data.loc[corr_clean.index]

	print "Predicting the unrated movies, please wait......"
	for user in corr_clean.index.values:
		noRating = data.ix[user]
		noRating = noRating[noRating.isnull()]			#movies that user never rated before
		corr_user = corr_clean[user].drop(user)			#drop user itself
		corr_user = corr_user[corr_user>0.1].dropna()	#pick corr_user that the correlation>0.1
		for movie in noRating.index:
			prediction = []
			for other in corr_user.index:
				if not np.isnan(data.ix[other, movie]):
					prediction.append((data.ix[other, movie], corr_clean[user][other]))
			if prediction:
				predicted_data[movie][user] = sum([value*weight for value, weight in prediction])/sum([pair[1] for pair in prediction])

	print "Writing predicted data into csv file, please wait......"
	res_path = os.path.join(os.getcwd(), '../res/preRatings.csv')
	predicted_data.to_csv(res_path)

	print "Done, please check your preRatings.csv in"+os.path.join(os.getcwd(), '../res')
	return predicted_data
	
def main():
	localPath = os.getcwd()
	srcPath = os.path.join(localPath, '../src/ratings.csv')
	print 'srcPath = ', srcPath
	predicted_data = CollaborativeFiltering(srcPath)

if __name__ == '__main__':
		main()	