#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
''' This module has a function to print nested list'''
def list_all(list_name, indent = 0):
    ''' print nested list 
        indent is the number of /t before print'''
    for item in list_name:
        if isinstance(item, list):
            list_all(item, indent+1)
        else:
            for n in range(indent):
                print('\t', end = '')
            print(item)
