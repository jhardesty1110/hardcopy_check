#! /usr/bin/env python

"""
  Author:  Jim Hardesty

  This script helps with hardcopy analysis.
  
  It gathers the necessary information to make hardcopy analysis easier.

"""


import sys, getopt
sys.path.append("/afs/data/bin/binpy")
import os
import DB2Queries
import types
import csv
import re
import subprocess
from bs4 import BeautifulSoup



def usage():
    print('''
    usage:

    hardcopy_check.py -p project_MH_SUBMIT_dir

    or

    while in the MH_SUBMIT directory,

    hardcopy_check.py [return]


    ''')


def main(argv):
    opt_p = ''     # path to the MH_SUBMIT directory

    try:
         opts, args = getopt.getopt(argv,"hp:", ["proj_dir="])
    except getopt.GetoptError:
         print 'Something went wrong, maybe wrong option letter'
	 print 'hardcopy_check.py -p project_MH_SUBMIT_dir'
	 sys.exit()

    for opt, arg in opts:
         if opt == '-h':
	      usage()
	      sys.exit()
	 elif opt in ('-p', '--proj_dir'):
	      opt_p = arg

    if opt_p == '':
         opt_p = os.getcwd()


    if not re.search("MH_SUBMIT", opt_p):
         print 'You are not in a MH_SUBMIT directory!\n'
	 sys.exit()

    premap_hardcopy_out_list = open(opt_p + "/Premap.hardcopy.out", "r")

    premap_hardcopy_out_list_contents = [line.rstrip() for line in premap_hardcopy_out_list]       #convert the text file into a list.  Takes out the newline character and trailing whitespace.


    chipedge_at_origin = []

    count = 0
    print ''
    for line in premap_hardcopy_out_list_contents:
         if "INFO:  CHIPEDGE AT 0,0" in line:
	      count += 1
	      print str(count) + " INFO:  CHIPEDGE AT 0,0"


    print "\n"
    count = 0

    for line in premap_hardcopy_out_list_contents:
         if "INFO:  NO DESIGN LEVEL DATA FOUND OUTSIDE CHIPEDGE" in line:
	      count += 1
	      print str(count) + " INFO:  NO DESIGN LEVEL DATA FOUND OUTSIDE CHIPEDGE"

    print "\n"
    count = 0

    for line in premap_hardcopy_out_list_contents:
         if "OK (no warning levels with data found...)" in line:
	      count += 1
	      print str(count) + " OK (no warning levels with data found...)"

    print "\n"
    count = 0

    for line in premap_hardcopy_out_list_contents:
         if "INFO:  ALL CHIP SIZES MATCH SKI.O!" in line:
	      count +=1
	      print "INFO:  ALL CHIP SIZES MATCH SKI.O!"
              print ''
    if count == 0:
         print ">>>> There is a potential chip size mis-match. <<<<"
         print ''

    
    master_layer_list = []

    item_iter = iter(premap_hardcopy_out_list_contents)     # make premap_hardcopy_out_list_contents iterable

    ordered_flag = "not_set"
    chip_count = 0
   
    print ''
    print "Ordered mask levels with no data:"

    for line in item_iter:
         if ordered_flag == "set":
	      if line.rstrip() == "":
	           ordered_flag = "not_set"
		   item_iter.next()
              else:
	           line2 = line.rstrip()     #remove trailing spaces
		   master_layer_list.append(line2)
		   print line2
         if ordered_flag == "not_set":
	      if "Ordered mask levels with no data:" in line:
	           ordered_flag = "set"
		   chip_count = chip_count + 1

		   #master_layer_list.append(" ")
                   print ""
		   line2 = re.sub(r'Ordered mask levels with no data:',"Chip_#" + str(chip_count) + " ",line)       #leaving just the layer list if not a multiple line list
		   master_layer_list.append(line2)
		   print line2

    print '\n'

    item_iter_2 = iter(premap_hardcopy_out_list_contents)
    master_layer_list2 = []
    ordered_flag = "not_set"
    chip_count = 0

    print "keywords with missing required levels:"

    for line in item_iter_2:
         if ordered_flag == "set":
	      if line.rstrip() == "":
	           ordered_flag = "not_set"
                   item_iter_2.next()
              else:
	           line2 = line.rstrip()     #remove trailing spaces
		   master_layer_list2.append(line2)
		   print line2
	 if ordered_flag == "not_set":
	      if "keywords with missing required levels:" in line:
	           ordered_flag = "set"
		   chip_count = chip_count + 1
		   print ""
		   line2 = re.sub(r'keywords with missing required levels:',"Chip_#" + str(chip_count) + " ",line)  #leaving just the layer list if not a multiple line list
		   master_layer_list2.append(line2)
		   print line2


    print ''




    #print master_layer_list


    premap_hardcopy_out_list.close()


if __name__ == '__main__':

    main(sys.argv[1:])

