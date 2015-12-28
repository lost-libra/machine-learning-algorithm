#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pandas as pd
import os

def main():
	user_genres_path = 'ml-1m/user_genres_data.csv'
	user_genres_data = pd.read_csv(user_genres_path, header = 0, index_col = 0)
	rating_path = 'ml-1m/smallratings.dat'
	ratings = pd.read_table(rating_path, sep = ',', header = 0, index_col = 0)

	print user_genres_data.index
	print ratings.index
	#print 'user_count = ', ratings.count(axis = 1)
	#print 'movie_count = ', ratings.count()3662

if __name__ == '__main__':
	main()