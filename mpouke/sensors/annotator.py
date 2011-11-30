import csv

gestures = csv.reader(open('gestureteachdata1811.csv'), delimiter=',')
annotations = csv.reader(open('gestureteach1811.csv'), delimiter=',')
newfile = csv.writer(open('1811teachset.csv', 'wb'), delimiter=',')


def msconvert(annotime):
	s = annotime
	hours, minutes, seconds = (["0", "0"] + s.split(":"))[-3:]
	hours = int(hours)
	minutes = int(minutes)
	seconds = float(seconds)
	miliseconds = int(3600000 * hours + 60000 * minutes + 1000 * seconds)
	return miliseconds


for row in annotations:
	annotime = row[0]
	annotation = row[1]
	#annotation = row[1]
	newlist=[]

	#print annotime
	annoms = msconvert(annotime)
	print annoms, annotation
	r=gestures.next()
	gestime = r[0]
	ax = r[1]
	ay = r[2]
	az = r[3]
	gx = r[4]
	gy = r[5]
	gz = r[6]
	#print gestime
	#print ' '
	newlist = annotime,ax,ay,az,gx,gy,gz,annotation
	#newlist.append(annotation)
	newfile.writerow(newlist)
	while int(gestime)<int(annoms):
		r=gestures.next()
		gestime = r[0]
		ax = r[1]
		ay = r[2]
		az = r[3]
		gx = r[4]
		gy = r[5]
		gz = r[6]
		newlist = annotime,ax,ay,az,gx,gy,gz,annotation
		#newlist.append(annotation)
		newfile.writerow(newlist)
		#print gestime

