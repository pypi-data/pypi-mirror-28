﻿'''
Created on 2017年12月15日

@author: Johnson
'''
#coding=utf-8 
#-*-coding:utf-8-*-

"""这是一个'06DefPrintList01.py'模块，提供了一个名为print_nesterlist()的函数，作用是打印列表的数据项，其中可能包含（也可能不包含）嵌套列表"""
def print_nesterlist(the_list,indent=False,level=0):         #定义函数,包括列表，嵌套，级别三个参数
    '''这个函数取一个位置参数，名为"the_list",它可以是任何Python列表（也可是包含嵌套列表的列表）。所指定的列表中的每个数据项会（递归地）打印输出，各数据项各占一行。
    第2个参数（名为“level”）用来在遇到嵌套列表时插入制表符TAB缩进'''
    for each_item in the_list:          #用一个“for”循环处理所提供的列表
        if isinstance(each_item, list): #判断列表数据项是否为列表
            print_nesterlist(each_item,indent,level+1) #如果是，调用本函数,每次处理一个嵌套列表时，都需将level的值加1
        else:
        #否则                           
            if indent:                        #如果indent为True，进行缩进
                for tab_stop in range(level):
                    print("\t",end='')        #打印制表符（TAB）
            print(each_item)                  #在屏幕上打印显示这个列表项
