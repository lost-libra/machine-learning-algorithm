#coding=utf-8
import os, csv

src_path = os.path.join(os.getcwd(), "ratings.csv")
dest_path = os.path.join(os.getcwd(), "smallratings.csv")

with open(src_path, 'rb') as ratings:
	reader = csv.reader(ratings)
	with open(dest_path, 'wb') as myratings:
		spamwriter = csv.writer(myratings)
		for row in reader:
			try:
				movieid = int(row[1])
				userid = int(row[0])
			except:
				movieid = -1
				userid = -1
			if movieid>1000:
				continue
			if userid>100:
				break
			spamwriter.writerow(row)