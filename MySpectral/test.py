#coding=utf-8

import numpy as np
import pandas as pd
import os


#读取MovieLens的数据
path = os.path.join(os.getcwd(),"src/smallratings.csv")

ratingData = pd.read_csv(path, header=0)
print type(ratingData)
rt = ratingData.pivot(index='userId', columns='movieId', values='rating')
print rt
#print ratingData.loc[:, ["userId", "movieId"]]