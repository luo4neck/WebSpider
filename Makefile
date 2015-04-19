all: store_csv.py

test:
	python store_csv.py http://movie.douban.com/people/blacktea077/collect

clean:
	rm *.csv
