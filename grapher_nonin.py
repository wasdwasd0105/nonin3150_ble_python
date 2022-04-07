import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import time

import os
import csv
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
import random
from collections import deque

curdir = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(curdir, '..', 'Data')
PLETH_FILE = 'pleth.csv'
PULSE_OX_FILE =  'pulse_ox.csv'

#to let the bluetooth connect and collect some data points
#time.sleep(15)

def make_ticklabels_invisible(fig):
    for i, ax in enumerate(fig.axes):
        ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
        for tl in ax.get_xticklabels() + ax.get_yticklabels():
            tl.set_visible(False)


gs = GridSpec(2, 2)
# build a rectangle in axes coords
left, width = .25, .5
bottom, height = .25, .5
right = left + width
top = bottom + height

#all graph variables for foot

xar = deque(maxlen = 500) # forces x array to fixed sz
yar = deque(maxlen = 500) # forces y array to fixed sz
xar1 = deque(maxlen = 500) # forces x array to fixed sz
yar1 = deque(maxlen = 500) # forces y array to fixed sz
xar2 = deque(maxlen = 500) # forces x array to fixed sz
yar2 = deque(maxlen = 500) # forces y array to fixed sz
i = 0



fig = plt.figure()
ax1 = fig.add_subplot(212)
axr = fig.add_axes([0.5,0.75,0.5,0.25])
axl = fig.add_axes([0,0.75,0.5,0.25])

pl = patches.Rectangle(
    (left, bottom), width, height,
    fill=False, transform=axl.transAxes, clip_on=False
    )
pr = patches.Rectangle(
    (left, bottom), width, height,
    fill=False, transform=axr.transAxes, clip_on=False
    )

axr.add_patch(pr)
axl.add_patch(pl)

axr.set_xticklabels([])
axl.set_xticklabels([])

axr.axis('off')
axl.axis('off')

def animate(i):
    #create graph
    try:
        #pull data from the file
        pullData = open(PLETH_FILE,"r").read() #pleth-hand
        pullData2 = open(PULSE_OX_FILE,"r").read() #pulse-ox-hand

        #Splitting up the data
        dataArray = pullData.split('\n')
        dataArray2 = pullData2.split('\n')

        #for the big plot in the bottom
        xar.clear()
        yar.clear()

        for eachLine in dataArray:
            if len(eachLine)>1:
                row = eachLine.split(',')
                idx = 1
                for val in [x + i * 23 for x in range(1,24)]:
                    xar.append(val)
                    yar.append(int(row[idx]))
                    idx += 1
                i += 1

        ax1.clear()
        ax1.plot(xar,yar)

        #print('Plot big')
        # rescales window to create the 'sliding window' effect
        ax1.relim()
        ax1.autoscale()

        #---------------------------------------------------------------------------
        #for the two plots in row one
        xar1.clear()
        yar1.clear()
        xar2.clear()
        yar2.clear()

        for eachLine1 in dataArray2:
            if len(eachLine1) > 1:
                row1 = eachLine1.split(',')
                xar1.append(i)
                yar1.append(int(row1[5])) #SPO2
                xar2.append(i)
                yar2.append(int(row1[3])) #PAI

        axl.clear()
        axr.clear()
        #SPO2
        axl.text(0.5*(left+right), 0.5*(bottom+top), str(yar1[-1]),
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=10, color='red',
            transform=axl.transAxes)

        axl.text(0.75 * right, top, 'SPO2 - hand',
            horizontalalignment='right',
            verticalalignment='top',
            transform=axl.transAxes)

        #PAI
        axr.text(0.5*(left+right), 0.5*(bottom+top), str(yar2[-1]),
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=10, color='red',
            transform=axr.transAxes)

        axr.text(0.75 * right, top, 'PAI - hand',
            horizontalalignment='right',
            verticalalignment='top',
            transform=axr.transAxes)

        axr.set_axis_off()
        axl.set_axis_off()

        print(yar1[-1])
        print(yar2[-1])
    except:
        print('File not found')

ani = animation.FuncAnimation(fig, animate, interval=500)
plt.show()
