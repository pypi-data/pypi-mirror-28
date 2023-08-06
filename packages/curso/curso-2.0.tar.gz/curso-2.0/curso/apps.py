# -*- coding: utf-8 -*-
from django.apps import AppConfig
import urllib, requests, json
from timetable.models import Course
from ngram import NGram

class SearchConfig(AppConfig):
    name = 'curso'
    
class SearchOb(object):
	"""docstring for SearchOb"""
	def __init__(self, uri=None):
		from pymongo import MongoClient
		self.client = MongoClient(uri)
		self.db = self.client['timetable']
		self.SrchCollect = self.db['CourseSearch']
		self.cursoNgram = NGram((i['key'] for i in self.SrchCollect.find({}, {'key':1, '_id':False})))

	def search(self, keyword, school):
		cursor = self.SrchCollect.find({'key':keyword, 'school':school}, {'value':1, '_id':False}).limit(1)
		if cursor.count() > 0:
			# Key Exist
			pass
		else:
			keyword = self.cursoNgram.find(keyword)		
			cursor = self.SrchCollect.find({'key':keyword, 'school':school}, {'value':1, '_id':False}).limit(1)
		return cursor[0]['value']
