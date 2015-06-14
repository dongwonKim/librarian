#!/usr/bin/python

from threading import Thread, Lock
import serial
import time, thread
import os
import multiprocessing
from filelock import FileLock
from xbee import XBee

mutex = Lock()

def run_server(file_path):
	os.system(file_path);

file_path = '/root/web_server/helloworld.py'
p = multiprocessing.Process(target = run_server, args=(file_path,))
p.start()

use = 0
occupy = 1
free = 2

state = {occupy:'occupy', use:'use', free:'free'}
seat = {}


def counter(source_addr):
	time.sleep(10)
	if seat[source_addr]['state'] == occupy:
		seat[source_addr]['state'] = free
		file_write()

def file_write():
	mutex.acquire()
	f=open("/root/web_server/static/seats.xml", "w")
	f.write( '<?xml version="1.0" encoding = "utf-8"?>\n')
	f.write( "<seats>\n")
	for i in sorted(seat.keys()):
		f.write( '<seat name="seat'+str(i)+'">\n')
		f.write( "<number>"+str(i)+"</number>\n")
		f.write( "<type>"+state[seat[i]['state']]+"</type>\n")
		f.write( "</seat>\n")
	f.write("</seats>\n")
	print "file write"
	f.close()
	mutex.release()


def response_handle(source_addr):
	first_state = seat[source_addr]['state']
	print seat[source_addr]
	avg=sum(seat[source_addr]['sampling_datas'])/len(seat[source_addr]['sampling_datas'])
	print 'average =', avg
	if seat[source_addr]['state'] == free:
		if avg<950: return;
		else: 
			seat[source_addr]['state'] = use
	
	elif seat[source_addr]['state'] == use :
		if avg<950:
			seat[source_addr]['state'] = occupy
			thread.start_new_thread(counter, (source_addr, ))
			
	elif seat[source_addr]['state'] == occupy:
		if avg>950:
			seat[source_addr]['state'] = use
	
	if seat[source_addr]['state'] is not first_state:
		print "state change"
		file_write()

ser = serial.Serial('/dev/ttyO4', 9600)

xbee = XBee(ser)


while True:
    try:
        response = xbee.wait_read_frame()
	source_addr = ord(response['source_addr'][1])
	sampling_data = response['samples'][0]['adc-0']
        print response
	
	if source_addr not in seat:
		seat[source_addr] = {'state' : free, 'sampling_datas' : []}
		file_write();
		
	seat[source_addr]['sampling_datas'] += [sampling_data]
	
	if len(seat[source_addr]['sampling_datas']) > 10: seat[source_addr]['sampling_datas'] = seat[source_addr]['sampling_datas'][1:]
	response_handle(source_addr)
    except KeyboardInterrupt:
        break
p.terminate()        
ser.close()
