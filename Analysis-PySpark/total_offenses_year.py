from __future__ import print_function

import sys
from operator import add
from pyspark import SparkContext
from csv import reader

if __name__ == "__main__":
	sc = SparkContext()
	
	def toCSVLine(data):
		return ','.join(str(d) for d in data)
		
	def splityear(x):
		a = x.split('/')
		return a[2]		
    
	lines = sc.textFile(sys.argv[1], 1)

	lines = lines.mapPartitions(lambda x: reader(x))
	
	bronx = lines.filter(lambda x: x[2] == 'BRONX') \
			.map(lambda x: (splityear(x[0]), x[1], x[2])) \
			.map(lambda x: (x,1)).reduceByKey(add).sortByKey()
	
	brooklyn = lines.filter(lambda x: x[2] == 'BROOKLYN') \
			.map(lambda x: (splityear(x[0]), x[1], x[2])) \
			.map(lambda x: (x,1)).reduceByKey(add).sortByKey()	

	manhattan = lines.filter(lambda x: x[2] == 'MANHATTAN') \
			.map(lambda x: (splityear(x[0]), x[1], x[2])) \
			.map(lambda x: (x,1)).reduceByKey(add).sortByKey()

	queens = lines.filter(lambda x: x[2] == 'QUEENS') \
			.map(lambda x: (splityear(x[0]), x[1], x[2])) \
			.map(lambda x: (x,1)).reduceByKey(add).sortByKey()

	staten = lines.filter(lambda x: x[2] == 'STATEN ISLAND') \
			.map(lambda x: (splityear(x[0]), x[1], x[2])) \
			.map(lambda x: (x,1)).reduceByKey(add).sortByKey()			
	
	total_offenses_year_bronx = bronx.map(toCSVLine)
	total_offenses_year_brooklyn = brooklyn.map(toCSVLine)
	total_offenses_year_manhattan = manhattan.map(toCSVLine)
	total_offenses_year_queens = queens.map(toCSVLine)
	total_offenses_year_staten = staten.map(toCSVLine)
	
	total_offenses_year_bronx.saveAsTextFile('total_offenses_year_bronx.csv')
	total_offenses_year_brooklyn.saveAsTextFile('total_offenses_year_brooklyn.csv')
	total_offenses_year_manhattan.saveAsTextFile('total_offenses_year_manhattan.csv')
	total_offenses_year_queens.saveAsTextFile('total_offenses_year_queens.csv')
	total_offenses_year_staten.saveAsTextFile('total_offenses_year_staten.csv')