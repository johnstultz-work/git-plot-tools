#!/usr/bin/env python
# by: John Stultz <john.stultz@linaro.org>
# Copyright 2013 Linaro Limited
#
# Licensed under the GPLv2
#
# This tool requires matplotlib 1.0 or greater to be installed!

import time
import string
import sys
import matplotlib
matplotlib.use('Agg')
from pylab import *
from datetime import *
from distutils.version import StrictVersion

#make sure we've got a recent version fo matplotlib
if (StrictVersion(matplotlib.__version__) < StrictVersion('1.0')):
	print "Error: This tool requires matplotlib 1.0 or greater"
	sys.exit(-1)



#helpers for tweaking chart size/fonts
xbigchart	= {"dpi":500, "dotsize":2, "yfont":2, "grid_axis":"x", "othercut":7}
bigchart 	= {"dpi":200, "dotsize":4, "yfont":5, "grid_axis":"x", "othercut":5}
normchart	= {"dpi":200, "dotsize":6, "yfont":8, "grid_axis":"both", "othercut":2}

chart_opts = normchart


if len(sys.argv) < 2:
	print "Usage: ", sys.argv[0], " <filename>"
	print 'Where <filename> is the output file from a call to:'
	print '	git log --pretty="%at, %s" <range>'
	sys.exit(-1)


#Get the commit data
datafile = open(sys.argv[1], "r")
biglist = {}
for line in datafile.read().split("\n"):
	if not "," in line:
		continue
	(datestr,patch_type) = line.split(",", 1)

	datestr = float(datestr)
	date = datetime.fromtimestamp(datestr)

	# try to cleanup the patch_type
	patch_type = patch_type.strip()

	if "[PATCH]" in patch_type[0:8].upper(): #special case [PATCH] intro
		patch_type = patch_type[8:]

	patch_type = patch_type.split(":")[0]
	patch_type = patch_type.split(" ")[0]
	patch_type = filter(str.isalnum, patch_type)
	patch_type = patch_type.strip()
	patch_type = patch_type.lower()

	# add to biglist
	if (biglist.has_key(patch_type)):
		biglist[patch_type].append(date)
	else:
		biglist[patch_type] = [date]


#try to guess chart type from data set
if (len(biglist.keys()) > 150):
	chart_opts = bigchart
if (len(biglist.keys()) > 300):
	chart_opts = xbigchart


# group any list smaller then N items into "other"
biglist["other"] = []
for key in biglist.keys():
	tmplist = []
	if (len(biglist[key]) < chart_opts["othercut"]) :
		tmplist = biglist[key]
		biglist["other"] =  biglist["other"] + tmplist
		biglist.pop(key, None)

#now do the plotting
ticks=[]
colors = ['.r','.g','.b','.c','.m','.y']

#plot dots
count = 1; #start with 1 to avoid dots at the bottom edge
for key in biglist.keys():
	points = [count] * len(biglist[key])
	plot_date(biglist[key], points, colors[count%len(colors)],
					markersize=chart_opts["dotsize"])
	ticks.append(count)
	count = count +1
#add an empty list to avoid dots at the top edge
plot_date([], [], colors[count%len(colors)], markersize=chart_opts["dotsize"])
ticks.append(count)

#setup ticks/labels/fonts/etc
ax = subplot(111)
ax.set_ylim([0,count]) 
ax.set_yticks(ticks)
ax.set_yticklabels(biglist.keys())
ax.yaxis.set_ticks_position('right')
ax.tick_params(axis='y', which='major', labelsize=chart_opts["yfont"])
formatter = DateFormatter('%m/%y')
ax.xaxis.set_major_formatter(formatter)
labels = ax.get_xticklabels()
setp(labels, fontsize=8)
grid(axis=chart_opts["grid_axis"])

#output the chart
savefig('commit-chart.png', bbox_inches='tight', dpi=chart_opts["dpi"])
#show()

