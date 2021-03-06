#!/usr/bin/python
# -*- coding: utf-8 -*- 
__author__ = ['Oguz Yarimtepe <oguzy@gmail.com>', 'Mustafa Arici <cad@mustafaarici.info>']

''' This module is used for collecting processed data from any planet instance that is already ran.'''

from djagen.collector.models import *

class PlanetHandler():

    def __init__(self,planet):
        self.channels = planet.channels()

    def run(self):
        for channel in self.channels:
            self.author_ch = self.__DeliverChannelToDB(channel)
            for item in channel.items():
                self.__DeliverItemToDB(item,self.author_ch)
        self.__DeliverRunTimeToDB()

    def __DeliverChannelToDB(self,channel):
        """ This def. writes author and channel related bits into the DB. 
        You should provide at least a channel from planet.channels()
        This def. returns an author object-model related to DB
        """
        try:
            author = Authors.objects.get(author_id = channel.id )
        except:
            author = Authors(author_id=channel.id)
        finally:
            author.author_name = channel.name
            try:
                author.author_surname = channel.surname
            except:
                author.author_surname = ''
            author.channel_url = channel.url

            try:
                author.author_face = channel.face
            except:
                author.author_face = None
            try:
                author.channel_subtitle = channel.subtitle
            except:
                author.channel_subtitle = None
            try:
                author.channel_title = channel.title
            except:
                author.channel_title = None    
            try:
                author.channel_link = channel.link
            except:
                author.channel_link = None

            try:
                author.channel_urlstatus = channel.url_status
            except:
                author.channel_urlstatus = None

            if channel.label == "Personal":
                author.label_personal = 1
            if channel.label == "LKD":
                author.label_lkd = 1
            if channel.label == "Community":
                author.label_community = 1
            if channel.label == "Eng":
                author.label_eng = 1
            author.save()
            return author

    def __DeliverItemToDB(self,item,author):
        """ This def. writes entry and item related bits into the DB. 
        You should provide at least a an existing author object-model and an item from channel 
        This def. returns an entry object-model related to DB
        """
        try:
            entry = author.entries_set.get(id_hash = item.id_hash)
        except:
            d = item.date
            entry = author.entries_set.create(
                                              id_hash = item.id_hash,
                                              date =datetime.datetime(d[0], d[1], d[2], d[3], d[4], d[5]),
                                              )
        finally:
            try:
                entry.title = item.title
            except:
                entry.title = None
            try:
                entry.content_html = item.content
            except:
                entry.content_html = None
            try:
                entry.content_text = entry.sanitize(item.content)
            except:
                entry.content_text = None
            try:
                entry.summary = item.summary
            except:
                entry.summary = None
            try:
                entry.link = item.link
            except:
                entry.link = None
                d = item.date
                entry.date = datetime.datetime(d[0], d[1], d[2], d[3], d[4], d[5])
            entry.save()
            return entry

    def __DeliverRunTimeToDB(self):
        """ Passes the time to DB, which this script has runned at."""
        r = RunTime()
        r.save()
