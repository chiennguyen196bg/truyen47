# -*- coding: utf-8 -*-
import requests
from lxml import html
import time
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
	try:
		response = requests.get(url)
	except:
		f = open('public/urlerr.txt','a')
		f.write(url+'\n')
		f.close()
	else:
		if response.status_code == 200: # Response Code  
			chap = {}
			parsed_body = html.fromstring(response.text)
			try:
			# lay tieu de
				word = parsed_body.xpath('//*[@id="trang_doc"]/div[@class="hentry"]/h1/text()')
				chap['name'] = word[0]
				chap['slug'] = slugify(chap['name'])
				chap['content'] = parsed_body.xpath('//div[@class="vung_doc"]/img/@src')
				chap['_id'] = time.time()
				db.chap.insert_one(chap)
				return (chap['name'], chap['_id'], chap['slug'])
			except:
				pass
		else:
			print "Error:", url

def crawl_title(url, hot = False):
	try:
		response = requests.get(url)
	except:
		f = open('public/urlerr.txt','a')
		f.write(url+'\n')
		f.close()
	else:
		if response.status_code == 200: # Response Code  
			item = {}
			parsed_body = html.fromstring(response.text)
			try:
				item['name'] = parsed_body.xpath('//*[@id="main_body"]/div[2]/div/div[2]/div[1]/div[1]/ul/li[1]/h1/text()')
				if item['name'] == []:
					item['name'] = 'null'
				else:
					item['name'] = item['name'][0]
				item['slug'] = slugify(item['name'])
				# lay img thumb
				try:
					item['thumb'] = parsed_body.xpath('//*[@id="main_body"]/div[2]/div/div[2]/div[1]/div[1]/div/span[1]/img/@src')[0]
					try:
						imgData = ab.open(item['thumb']).read()
					except:
						f = open('public/urlerrthumb.txt','a',0)
						f.write(item['thumb']+'\n')
						f.close()
					else:
						f = open('public/images/'+item['slug']+'.jpg', 'wb')
						f.write(imgData)
						f.close()
				except:
					pass
				
				item['hot'] = hot
				item['author'] = parsed_body.xpath('//*[@id="main_body"]/div[2]/div/div[2]/div[1]/div[1]/ul/li[2]/a/text()')
				item['genres'] = parsed_body.xpath('//*[@id="main_body"]/div[2]/div/div[2]/div[1]/div[1]/ul/li[3]/a/text()')
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
			except:
				pass
			
		else:
			print "Error:", url


def add_chap_from_list(list_chap):
	chap_return = []
	for chap in list_chap:
		(chap_name, chap_id, chap_slug) = crawl_chapter(chap['link'])
		chap_temp = {'name': chap_name, 'id': chap_id, 'slug': chap_slug, 'type': chap['type']}
		chap_return.append(chap_temp)
	return chap_return

def del_chap_from_list(list_chap):
	for chap in list_chap:
		db.chap.delete_one({'_id' : chap['id']})
			
def lay_name(i):
	item = {}
	item['slug'] = slugify(parsed_body.xpath('//*[@id="main_body"]/div[3]/div[2]/div[%d]/h3/a/text()' % i)[0])
	item['link'] = parsed_body.xpath('//*[@id="main_body"]/div[3]/div[2]/div[%d]/h3/a/@href' % i)[0]
	list_type = parsed_body.xpath('//*[@id="main_body"]/div[3]/div[2]/div[%d]/h3/span/text()' % i)
	item['hot'] = item['new'] = False
	if 'Hot' in list_type:
		item['hot'] = True
	if 'New' in list_type:
		item['new'] = True
	return item


def lay_list_chap(i):
	list_chap = []
	length = len(parsed_body.xpath('//*[@id="main_body"]/div[3]/div[2]/div[%d]/a/text()' % i))
	for x in range(1, length + 1):
		chap = {}
		chap['slug'] = slugify(parsed_body.xpath('//*[@id="main_body"]/div[3]/div[2]/div[%d]/a[%d]/text()' % (i,x))[0])
		chap['link'] = parsed_body.xpath('//*[@id="main_body"]/div[3]/div[2]/div[%d]/a[%d]/@href' % (i,x))[0]
		typ = parsed_body.xpath('//*[@id="main_body"]/div[3]/div[2]/div[%d]/span/text()' % (i))
		if typ != []:
			chap['type'] = typ[0]
		else:
			chap['type'] = None
		list_chap.append(chap)
		re = add_chap_from_list(list_chap[::-1])
	return re



if __name__ == '__main__':
	url = raw_input("url: ")
	crawl_title(url)