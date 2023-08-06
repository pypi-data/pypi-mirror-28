# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import inspect


class Webhook (models.Model):

    def __getattr__(self, name):
        def method(*args):
            print("tried to handle unknown method " + name)
            if args:
                print("it had arguments: " + str(args))
        return method

    def add(self):
        print self.__class__.__name__
        print inspect.currentframe().f_code.co_name

    '''
    def delete(self):
        pass

    def edit(self):
        pass

    def events(self):
        pass

    def list(self):
        pass

    def view(self):
        pass
    '''
