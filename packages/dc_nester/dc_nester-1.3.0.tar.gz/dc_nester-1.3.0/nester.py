#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
''' This module has a function to print nested list'''
def list_all(list_name, indent = False, tabstop = 0):
    ''' print nested list 
        use indent or not
        tabstop is the number of /t before print'''
    for item in list_name:
        if isinstance(item, list):
            list_all(item, indent, tabstop + 1)
        else:
            if indent: 
                print('\t' * tabstop, end = '')
            print(item)
