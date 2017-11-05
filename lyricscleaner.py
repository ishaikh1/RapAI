import requests
from bs4 import BeautifulSoup
import glob
import os

def clean_lyrics(page_name):
	"""A function to scrap a given genius.com page for lyrics.
	   Appends lyrics into a .txt file with the name of the song.
	   Appends lyrics to the end of allSongs(years).txt
	   Inputs:
	   page_name is a String representing a page to be scraped
	   for lyrics.
	 """
	page = requests.get(page_name)
	soup = BeautifulSoup(page.content, 'html.parser')

	artist = soup.find('a', class_='header_with_cover_art-primary_info-primary_artist').get_text()
	
	song_title = soup.find('h1', class_='header_with_cover_art-primary_info-title').get_text()

	soup = soup.find('div', class_='lyrics')
	soup = soup.select('p')


	lyrics = ''
	for i in soup:
		lyrics += i.get_text()
	lyrics = list(lyrics)

	for k in range(len(lyrics)):
		if(k < len(lyrics)):
			if (lyrics[k] == '['):
				while (lyrics[k] != ']'):
					del lyrics[k]
				del lyrics[k]
			elif (lyrics[k] == '('):
				while (lyrics[k] != ')'):
					del lyrics[k]
				del lyrics[k]

	for j in range(len(lyrics)):
		if(j+1 < len(lyrics)):
			if lyrics[j] == '?' and lyrics[j+1] != ' ':
				lyrics[j] = '? '
			elif lyrics[j] == '!' and lyrics[j+1] != ' ':
				lyrics[j] = '! '
			elif lyrics[j] == '\"':
				lyrics[j] = ''
			elif lyrics[j] == ',' and lyrics[j+1] != ' ':
				lyrics[j] = ', '
			elif (lyrics[j] == 'I') and lyrics[j+2] == '\'':
				lyrics[j+1] = ''
			elif lyrics[j] == '.' and lyrics[j-1] == ' ':
				lyrics[j-1] = ''
			elif (lyrics[j] == '\'') and (lyrics[j-1] == ' '):
				lyrics[j-1] = ''
			elif (lyrics[j] == '\n') and (lyrics[j-1] == '\n'):
				lyrics[j] = ''

		if (j+1 != len(lyrics)):
			if  (lyrics[j] in 'abcdefghijklmnopqrstuvwxyz') and (lyrics[j+1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
				lyrics[j] = lyrics[j] + '\n'



	lyrics = ''.join(lyrics)
	file_path = '1990-1999/' + 'Sir Mix-a-Lot' + '/Mack Daddy/' + song_title + '.txt'
	file = open(file_path, 'w')
	file.write(lyrics)
	file.close()

	all_songs = open('1990-1999/AllSongs/all1990-1999.txt', 'a')
	all_songs.write(lyrics)
	all_songs.close()

def get_album(album_page):
	"""A function to quickly scrape a whole album on genius.com
	   Uses clean_lyrics and a for loop.
	   Inputs:
	   album_name is a String representing the page of an album
	   to be scraped for lyrics.
	 """
	links = []
	page = requests.get(album_page)
	soup = BeautifulSoup(page.content, 'html.parser')
	soup = soup.find_all('a', class_='u-display_block')
	for i in soup:
		if(i.has_attr('href')):
			if ('lyrics' in i['href']) and ('album-art' not in i['href']) and ('remix' not in i['href']) and ('[credits]' not in i['href']) and ('[Credits]' not in i['href']) and ('[Booklet]' not in i['href']):
				links += [i['href']]
	for k in links:
		clean_lyrics(k)

def get_lyrics(era, artist, albums):
	"""Quickly compile all lyrics for an artist into one file.
	   Inputs:
	   era is a string representing years of songs being compiled.
	   artist is a string representing whose songs are to be compiled
	   albums is a list of albums representing albums of songs to be compiled from.
	 """
	for i in albums:
		files = glob.glob(era + '/' + artist + '/' + i + '/*.txt')
		allFile = open(era + '/' + artist + '/' + 'all' + artist + '.txt', 'a')
		for fle in files:
			with open(fle) as f:
				text = f.read()
			allFile.write(text)

# with open('2010-2017/AllSongs/all2010-2017.txt') as f:
#     content = f.readlines()
# prevline=''
# for line in content:
# 	if line == '\n' and prevline == '\n':
# 		line = ''
# 		prevline = ''
# 	prevline = line

# content = ''.join(content)
# print(content)
# text_file = open("2010-2017/AllSongs/all2010-2017.txt", "w")
# text_file.write(content)
# text_file.close()


get_lyrics('1990-1999', 'Wu-Tang-Clan', ['Enter the Wu-Tang'])
# get_lyrics('1990-1999', 'Dr. Dre', 'The Aftermath')

