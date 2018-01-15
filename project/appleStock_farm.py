"""
To execute on a Farm machine:
time spark-submit --packages com.databricks:spark-csv_2.11:1.5.0 appleStock_farm.py 2> /dev/null
"""

from pyspark import SparkContext
from pyspark.sql import SQLContext

stockFile = "file:///home/s2000032/aapl-apple-historicalStock.csv"
sc = SparkContext("local", "Stock")

sqlc = SQLContext(sc)
#.option("mode", "DROPMALFORMED") \
stockData = sqlc.read.format('com.databricks.spark.csv') \
    .options(header='true') \
    .option("inferschema", 'true') \
    .option("encoding", "UTF-8") \
    .load(stockFile)

stockData.printSchema()
print stockData.take(10)
