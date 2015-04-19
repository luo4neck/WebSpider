#! /usr/bin/python
import urllib2
import bs4
import time
import re
import csv
from sys import argv

def writer_csv(DICT):
	writer = csv.writer(file('MovieList.csv', 'wb'))
	for (k,v) in DICT.items():
		# print k, v
		writer.writerow([k, v])
# end of writer_csv..


def link_gen(i_get, userID):
	page_part1 = 'http://movie.douban.com/people/'
	page_part2 = '/collect?start='
	page_part3 = '&sort=time&rating=all&filter=all&mode=grid'
	page_link = page_part1 + userID + page_part2 + str(i_get * 15) + page_part3
	return page_link
# end of link_gen..


def load2dict(userID, page_max):
	opener = urllib2.build_opener()
	DICT = {} 

	i_get = 0 # this while is for new movie..
	while i_get < int(page_max): 
		page_link = link_gen(i_get, userID) 

		# get item id and name of the movie in this page..
		content = opener.open( page_link ).read().decode('utf-8')
		soup = bs4.BeautifulSoup(content)

		step_1 = soup.find( 'div', {'class' : 'grid-view'} )
		step_2 = step_1.findAll('li', { 'class': 'title' } )
	
		for item in step_2:
			m1 = re.search(r"\bsubject/\b(\d+)", str(item) )
			m2 = re.search(r"\bem\b[>](.+)['</']\bem\b", str(item) )
			DICT[int(m1.group(1))] =  m2.group(1).replace('<','')

		print '>>>>>>>>>>>>>> page', i_get, 'loaded'
		i_get = i_get + 1
		time.sleep(30) # sleep for half min..
		# while loop end..
	
	print 'Number of movies in new account: %d' % len(DICT)
	print 'Totally loaded.'
	return DICT
# end of load2dict..


def input_check(argv):
	if len(argv) > 2: # todo.. add more checks..
		print 'wrong input!'
		exit()

	# us re to get the userid
	re1='.*?'	# Non-greedy match on filler
	re2='((?:[a-z][a-z]*[0-9]+[a-z0-9]*))'	# Alphanum 1
	rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
	m = rg.search(argv[1])
	userID = m.group(1)
	# us re to get the userid

	# get the max page of the guy..
	opener = urllib2.build_opener()
	content = opener.open( argv[1] ).read().decode('utf-8')
	soup = bs4.BeautifulSoup(content)
	step_2 = soup.find('span', { 'class': 'thispage' } )
	maxpage = step_2['data-total-page']
	# get the max page of the guy..
	
	res = (userID, str( int(maxpage)+3) )
	print 'User ID: ', userID 
	print 'Totally pages: ', maxpage 
	return res
# end of input check..


if __name__ == '__main__':
	res = input_check(argv)
	DICT = load2dict( res[0], res[1] )
	writer_csv(DICT)
