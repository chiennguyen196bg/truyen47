# -*- coding: utf-8 -*-
import requests
from lxml import html
import time
import json
import sys
import gc
# from slugify import slugify
import json
import unicodedata,re

def slugify(str):
    slug = unicodedata.normalize("NFKD",unicode(str)).encode("ascii", "ignore")
    slug = re.sub(r"[^\w]+", " ", slug)
    slug = "-".join(slug.lower().strip().split())
    return slug

import mech
ab = mech.anonBrowser(proxies=[],\
			user_agents=[('user_agent', 'superSecretBroser')])

import pymongo
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.admin


def crawl_chapter(url):
	"""Lay noi dung chap"""
	for i in xrange(0, 3):
		try:
			response = requests.get(url)
			parsed_body = html.fromstring(response.text)
			word = parsed_body.xpath('//*[@id="trang_doc"]/div[@class="hentry"]/h1/text()')
			if word == []:
				raise NameError, "Khong lay duoc info chap"
		except NameError, e:
			print (e)
		except:
			f = open('public/urlerr.txt','a')
			f.write(url+'\n')
			f.close()
		else:
			chap = {}
			# lay tieu de
			word = parsed_body.xpath('//*[@id="trang_doc"]/div[@class="hentry"]/h1/text()')
			chap['name'] = word[0]
			chap['slug'] = slugify(chap['name'])
			chap['content'] = parsed_body.xpath('//div[@class="vung_doc"]/img/@src')
			chap['_id'] = time.time()
			db.chap.insert_one(chap)
			return (chap['name'], chap['_id'], chap['slug'])
			del chap
		time.sleep(5)
	return None, None, None

def crawl_truyen(url):
	for x in xrange(0, 3):
		try:
			response = requests.get(url)
			parsed_body = html.fromstring(response.text)
			check = parsed_body.xpath('//*[@id="main_body"]/div[2]/div/div[2]/div[1]/div[1]/ul/li[1]/h1/text()')
			if check == []:
				raise NameError, "Khong lay duoc info truyen"
		except NameError, e:
			print (e)
		except:
			f = open('public/urlerr.txt','a')
			f.write(url+'\n')
			f.close()
		else:
			item = {}
			
			item['name'] = parsed_body.xpath('//*[@id="main_body"]/div[2]/div/div[2]/div[1]/div[1]/ul/li[1]/h1/text()')[0]
			item['slug'] = slugify(item['name'])
			# lay img thumb
			item['thumb'] = parsed_body.xpath('//*[@id="main_body"]/div[2]/div/div[2]/div[1]/div[1]/div/span[1]/img/@src')[0]
			try:
				imgData = ab.open(item['thumb']).read()
			except:
				print "khong lay duoc thumb"
			else:
				try:
					f = open('public/images/'+item['slug']+'-truyen47.com.jpg', 'wb', 0)
					f.write(imgData)
				except Exception, e:
					print e
				finally:
					f.close()
			item['author'] = []
			author = parsed_body.xpath('//*[@id="main_body"]/div[2]/div/div[2]/div[1]/div[1]/ul/li[2]/a/text()')
			for i in xrange(0, len(author)):
				temp = {}
				temp['name'] = author[i]
				temp['slug'] = slugify(author[i])
				item['author'].append(temp)
				del temp
			del author

			item['genres'] = []
			genres = parsed_body.xpath('//*[@id="main_body"]/div[2]/div/div[2]/div[1]/div[1]/ul/li[3]/a/text()')
			for i in xrange(0, len(genres)):
				temp = {}
				temp['name'] = genres[i]
				temp['slug'] = slugify(genres[i])
				item['genres'].append(temp)
				del temp
			del genres

			item['status'] = parsed_body.xpath('//*[@id="main_body"]/div[2]/div/div[2]/div[1]/div[1]/ul/li[4]/a/text()')[0]

			item['summary'] = parsed_body.xpath('/html/head/meta[10]/@content')[0]
			if(item['summary'].find('Mangak.net') != -1):
				item['summary'] = ''

			item['chapter'] = []
			list_chap = parsed_body.xpath('//*[@id="main_body"]/div[2]/div/div[2]/div[2]/div[2]/div/span[1]/a/@href')
			list_chap = list_chap[::-1]
			for urlchap in list_chap:
				(chap_name, chap_id, chap_slug) = crawl_chapter(urlchap)
				chap = {'name': chap_name, 'id': chap_id, 'slug': chap_slug}
				item['chapter'].append(chap)
			item['lastChap'] = item['chapter'][len(item['chapter'])-1]
			return db.truyen.insert_one(item).inserted_id
		time.sleep(5)

def add_chap_from_list(list_chap_urls):
	chap_return = []
	for url in list_chap_urls:
		(chap_name, chap_id, chap_slug) = crawl_chapter(url)
		chap_temp = {'name': chap_name, 'id': chap_id, 'slug': chap_slug}
		chap_return.append(chap_temp)
	return chap_return

def del_chap_from_list(list_chap):
	for chap in list_chap:
		db.chap.delete_one({'_id' : chap['id']})
			

def main():
	list_items = []

	#doc file
	f = open('first_slug.txt','r')
	first_slug = f.read()
	f.close()
	first_slug = slugify(first_slug)

	try:
		# response = ab.open('http://mangak.net').read()
		response = requests.get('http://mangak.net')
		parsed_body = html.fromstring(response.text)
		check = parsed_body.xpath('//*[@id="main_body"]/div[3]/div[2]/div[1]/h3/a/text()')
		if check == []:
			raise NameError, "Notthing here"
	except Exception, e:
		print (e)
	else:
		#begin
		
		for i in xrange(1,46):
			item = {}
			item['slug'] = slugify(parsed_body.xpath('//*[@id="main_body"]/div[3]/div[2]/div[%d]/h3/a/text()' % i)[0])
			if item['slug'] == first_slug:
				del item
				break
			typ = parsed_body.xpath('//*[@id="main_body"]/div[3]/div[2]/div[%d]/span/text()' % (i))
			if typ != []:
				del item
				continue
		
			item['link'] = parsed_body.xpath('//*[@id="main_body"]/div[3]/div[2]/div[%d]/h3/a/@href' % i)[0]
			item['list_chap_urls'] = parsed_body.xpath('//*[@id="main_body"]/div[3]/div[2]/div[%d]/a/@href' % i)
			
			item['list_chap_urls'] = item['list_chap_urls'][::-1]
			list_items.append(item)
			del item

	while list_items:
		item = list_items.pop()
		result = db.truyen.find_one({'slug': item['slug']})
		if result == None:
			crawl_truyen(item['link'])
		else:
			chap_added = add_chap_from_list(item['list_chap_urls'])
			length_chapter = len(result['chapter'])
			index = length_chapter - 1
			while index > -1:
				if result['chapter'][index]['slug'] == chap_added[0]['slug']:
					break
				index = index - 1
			else:
				index = length_chapter
			del length_chapter

			del_chap_from_list(result['chapter'][index:])
			result['chapter'] = result['chapter'][0:index] + chap_added
			del chap_added
			del index
			result['lastChap'] = result['chapter'][len(result['chapter']) - 1]
			db.truyen.replace_one({'_id': result['_id']}, result)
		print item['slug']
		if not list_items:
			f = open('first_slug.txt','w',0)
			f.write(item['slug'])
			f.close()
			del item
			del result
	del list_items
	gc.collect()

if __name__ == '__main__':
	main()
	print "Everthings is Done!"