# -*- coding: utf-8 -*-
import requests
from lxml import html
import time
import json
import sys
import gc
import json
import unicodedata,re

def slugify(str):
	# if str == 'Huyền Huyễn':
	# 	return 'huyen-huyen'

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
			word = parsed_body.xpath('//div[@class="box container chap-container hentry"]/div/h1/text()')
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
			word = parsed_body.xpath('//div[@class="box container chap-container hentry"]/div/h1/text()')
			chap['name'] = word[0]
			chap['slug'] = slugify(chap['name'])
			chap['_id'] = time.time()
			#lay noi dung
			chap['content'] = parsed_body.xpath('//div[@class="box container chap-container hentry"]/div/div[2]/div[2]/img/@src')
			# print chap
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
			check = parsed_body.xpath('//div[@class="hentry"]/ul/li[2]/h1/text()')
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
			
			item['name'] = parsed_body.xpath('//div[@class="hentry"]/ul/li[2]/h1/text()')[0]
			item['slug'] = slugify(item['name'])
			# lay img thumb
			item['thumb'] = parsed_body.xpath('//div[@class="hentry"]/ul/li[1]/div/img/@src')[0]
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
			del item['thumb']
			
			item['author'] = []
			author = parsed_body.xpath('//div[@class="hentry"]/ul/li[3]/span/a/text()')
			for i in xrange(0, len(author)):
				temp = {}
				temp['name'] = author[i]
				temp['slug'] = slugify(author[i])
				item['author'].append(temp)
				del temp
			del author

			item['genres'] = []
			genres = parsed_body.xpath('//div[@class="hentry"]/ul/li[5]/a/text()')
			for i in xrange(0, len(genres)):
				temp = {}
				temp['name'] = genres[i]
				temp['slug'] = slugify(genres[i])
				item['genres'].append(temp)
				del temp
			del genres

			item['status'] = parsed_body.xpath('//div[@class="hentry"]/ul/li[6]/a/text()')[0]
			item['summary'] = parsed_body.xpath('/html/head/meta[10]/@content')[0]
			if(item['summary'].find('Truyentranhmoi.com') != -1):
				item['summary'] = ''

			item['chapter'] = []
			list_chap = parsed_body.xpath('//div[@class="box chap-list"]/ul/li/a/@href')
			# print list_chap
			list_chap = list_chap[::-1]
			for urlchap in list_chap:
				(chap_name, chap_id, chap_slug) = crawl_chapter(urlchap)
				chap = {'name': chap_name, 'id': chap_id, 'slug': chap_slug}
				item['chapter'].append(chap)
			item['lastChap'] = item['chapter'][len(item['chapter'])-1]
			return db.truyen.insert_one(item).inserted_id
			del item
		time.sleep(5)

def crawl_list_urls(url):
	for x in xrange(0, 3):
		try:
			response = requests.get(url)
			parsed_body = html.fromstring(response.text)
			list_urls = parsed_body.xpath('//div[@class="box chap-list truyen-list"]/ul/li/a[2]/@href')
			if list_urls == []:
				raise NameError, "Khong lay duoc info truyen"
			else:
				del response
				del parsed_body
				return list_urls
				del list_urls
		except Exception, e:
			print e


def main(list_truyen_urls):
	for url in list_truyen_urls:
		info = crawl_truyen(url)
		print info
		del info
		time.sleep(5)
	gc.collect()

if __name__ == '__main__':
	for i in range(1,54):
		urlList = 'http://truyentranhmoi.com/danh-sach/page/%d/' % i
		listUrlPage = crawl_list_urls(urlList)
		print i
		try:
			main(listUrlPage)
		except Exception, e:
			print e
		del urlList
		del listUrlPage
	gc.collect()
	print "Done"
		