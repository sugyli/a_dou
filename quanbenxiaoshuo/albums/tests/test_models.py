#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from test_plus.test import TestCase

from albums.models import Category,Album

from django.shortcuts import reverse
import random

class CategoryModelsTest(TestCase):

    def setUp(self):
        """初始化操作"""
        name='中文'+str(random.randint(0, 10000))

        self.category = Category.objects.create(
            name=name,
            title="title1",
            keywords="keywords1",
            description='description1',
        )
        print(self.category.slug)

    def test_object_instance(self):
        """判断实例对象是否为Article类型"""
        assert isinstance(self.category, Category)

    def test_get_category_url(self):
        self.assertEqual(self.category.get_category_url(), reverse('albums:category', args=[self.category.slug]))



class AlbumModelsTest(TestCase):
    def setUp(self):
        """初始化操作"""
        name='中文'+str(random.randint(0, 10000))

        self.category = Category.objects.create(
            name=name,
            title="title1",
            keywords="keywords1",
            description='description1',
        )
        album_name='专辑'+str(random.randint(0, 10000))

        self.album = \
            Album.objects.create(
                category=self.category,
                name=album_name,
                info='简介',
                title="title1",
                keywords="keywords1",
                description='description1',

            )

    def test_get_album_url(self):
        self.assertEqual(self.album.get_album_url(), reverse('albums:album', args=[self.album.slug]))

