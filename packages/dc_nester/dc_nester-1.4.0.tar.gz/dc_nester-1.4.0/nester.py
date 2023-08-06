#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
''' This module has a function to print nested list'''
import sys
def list_all(list_name, indent = False, tabstop = 0, output = sys.stdout):
    ''' print nested list 
        use indent or not
        tabstop is the number of /t before print
        output used to specify where to output'''
    for item in list_name:
        if isinstance(item, list):
            list_all(item, indent, tabstop + 1, output)
        else:
            if indent: 
                print('\t' * tabstop, end = '', file = output)
            print(item, file = output)
