#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
''' This module has a function to print nested list'''
def list_all(list_name):
    ''' print nested list '''
    for item in list_name:
        if isinstance(item, list):
            list_all(item)
        else:
            print(item)
