#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from django.test import Client
from django.urls import reverse
from test_plus.test import TestCase

from albums.models import Category
import random

class CategoryViewsTest(TestCase):

    def setUp(self):
        """初始化操作"""
        name='中文'+str(random.randint(0, 10000))

        self.category = Category.objects.create(
            name=name,
            title="title1",
            keywords="keywords1",
            description='description1',
        )


