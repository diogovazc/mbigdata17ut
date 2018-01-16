"""
This computes the asins of products containing a certain word in title across the
amazon products in the HDFS file /data/doina/UCSD-Amazon-Data/meta_Electronics.json.gz

To execute on a Farm machine:
time spark-submit getReviews_farm.py [user] [company] 2> /dev/null
"""

import sys
user = sys.argv[1]
company = sys.argv[2]
beginTime = sys.argv[3] if (len(sys.argv) > 4) else 1356998400
endTime = sys.argv[4] if (len(sys.argv) > 4) else 1388534399

from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import approxCountDistinct, countDistinct, col, avg


metaFile = '/data/doina/UCSD-Amazon-Data/meta_Electronics.json.gz'
reviewsfile = 'file:///home/' + user + '/reviews_Electronics.json.gz'

sc = SparkContext("local", "AmazonReviews")
sqlc = SQLContext(sc)

df = sqlc.read.json(metaFile)
products = df.select("asin", "title", "price")
meta = products.filter(products.title.rlike('(?i).*' + company + '.*')) 	\
	.filter(products.price > 50)

df2 = sqlc.read.json(reviewsfile)
reviews = df2.select('asin', "overall", "summary", "unixReviewTime", "reviewTime") \
	.filter(df2.unixReviewTime > beginTime) \
	.filter(df2.unixReviewTime < endTime)

reviews = reviews.join(meta, "asin")

print reviews.take(10)