#!/usr/bin/python
#
# pomodoro.py: a little script to help your productivity.
# Shaddi Hasan, 2010. http://sha.ddih.org.
#
# pomodoro.py is a simple script to help increase your focus and productivity.
# After you run the script, you'll have ten minutes of uninterrupted work time,
# which is enforced by disabling your network adapters. When ten minutes is up,
# you've earned a two minute break, and your network adapters will be brought
# back up. 
#
# To run this, make sure you have the required imports on your system, then 
# modify the interfaces lists below to reflect the names of your system's 
# network adapters. Then run:
#
#          $ sudo pomodoro &
# 
# If you need to kill it, open up another terminal and kill the process (but 
# resist the temptation!). 
#
#
#  let's try to package this in stackoverflow.com/questions/728589/example-of-how-to-use-msilib-to-create-a-msi-file-from-a-python-module http://docs.python.org/2/library/msilib.html for windows after gui TODO
#


import pynotify
import os, time, socket
from inet_drivers import (
        get_ifaces, 
        is_iface_on, 
        turn_on_iface, 
        turn_off_iface
        )

# notifications  TODO these would be great in gui
pynotify.init("pomodoro.py")
work = pynotify.Notification("Here we go!","Time to get to work!")
work.set_timeout(3)
rest = pynotify.Notification("Break!","Good job! You earned a break!")
rest.set_timeout(3)

# timings  TODO want these in gui too could be fun!
SEC_TO_RUN = 3*60*60 # 3 hour total runtime
WORK_TIME = 10*60 # 10 minutes of work time
REST_TIME = 2*60 # 2 minutes of break time
END_TIME = int(time.time()) + SEC_TO_RUN

disable_network = True
disable_interrupts = True  # cannot kill on ^C

# modify the interfaces list to match your particular system...
def turn_off_internet(socket_file, interfaces):
    for interface in interfaces:
        turn_off_iface(socket_file, interface)

def turn_on_internet(socket_file, interfaces):
	for interface in interfaces:
        turn_on_iface(socket_file, interface)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sfd = s.fileno()
ifaces = filter(lambda x: re.match('^eth|wlan',x), 
        get_ifaces(sfd))

# Main loop
while int(time.time()) < END_TIME:
	try:
		# work for a bit
		work_start = int(time.time())
		work.show()
		while int(time.time()) < (work_start + WORK_TIME):
			if disable_network:
				turn_off_internet(sfd, ifaces)
			time.sleep(10)

		# now rest
		rest.show()
		if disable_network:
			turn_on_internet(sfd, ifaces)

		time.sleep(REST_TIME)

	except:
		if disable_interrupts:
			continue
		else:
			break

final_note = pynotify.Notification("That's the end of it!","Great job being productive!")
final_note.set_timeout(5)
final_note.show()
	


