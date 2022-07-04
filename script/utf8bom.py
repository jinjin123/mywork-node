#!/usr/bin/env python
# -*- coding: utf-8 -*-
#2018/05/31 检测文件是否是utf-8无bom格式的
import sys, codecs
 
 
def detectUTF8(file_name):
    state = 0
    line_num = 0
    file_obj = open(file_name)
    all_lines = file_obj.readlines()
    file_obj.close()
    for line in all_lines:
        line_num += 1
        line_len = len(line)
        for index in range(line_len):
            if state == 0:
                if ord(line[index]) & 0x80 == 0x00:  # 上表中的第一种情况
                    state = 0
                elif ord(line[index]) & 0xE0 == 0xC0:  # 上表中的第二种情况
                    state = 1
                elif ord(line[index]) & 0xF0 == 0xE0:  # 第三种
                    state = 2
                elif ord(line[index]) & 0xF8 == 0xF0:  # 第四种
                    state = 3
                else:
                    print "%s isn't a utf8 file,line:\t" % file_name + str(line_num)
                    sys.exit(1)
            else:
                if not ord(line[index]) & 0xC0 == 0x80:
                    print "%s isn't a utf8 file in line:\t" % file_name + str(line_num)
                    sys.exit(1)
                state -= 1
    if existBOM(file_name):
        print "%s isn't a standard utf8 file,include BOM header." % file_name
        sys.exit(1)
 
 
def existBOM(file_name):
    file_obj = open(file_name, 'r')
    code = file_obj.read(3)
    file_obj.close()
    if code == codecs.BOM_UTF8:  # 判断是否包含EF BB BF
        return True
    return False
 
if __name__ == "__main__":
    a = open('1.txt','r') 
    for x in a.readlines():
    	file_name = x.strip()
    	detectUTF8(file_name)

