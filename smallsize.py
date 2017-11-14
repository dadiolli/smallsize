# -*- coding: utf-8 -*-
##############################################################################
# Settings
##############################################################################

longsidemax = 720
fullsizepath = 'full_size'
smallsizepath = 'small'
mode = "log" # use print to see output on console as well.

##############################################################################
# Import some stuff
##############################################################################

import os, shutil, sys, time
from PIL import Image
from progress.bar import ShadyBar
from progress.spinner import MoonSpinner
reload(sys) # need to reload sys to set default encoding
sys.setdefaultencoding('utf-8')
timestamp, start_time = time.strftime("%Y%m%d-%H%M%S"), time.time()
errorcounter, processcounter, reducecounter, enlargecounter = 0, 0, 0, 0
with open ("resize_log_" + timestamp + ".txt", 'wb') as logfile:
	logfile.write(u'\ufeff' + '✳️ Started small size generator at ' + timestamp + '\n')

##############################################################################
# Define logging function
##############################################################################

def log(mode, message):
	with open("resize_log_" + timestamp + ".txt", 'a') as logfile:
			logfile.write(message)
	if mode == 'print':
		print(message)

def occ_resize_small(im, root, filename):
	sides = [im.width, im.height]
	# 1024, 2087
	longside = max(sides) * 1.0
	#log(mode,"❌  " + filename + ": Could not determine longest side.\n")
	factor = longside / longsidemax
	percent = round(1 / factor * 100,2)
	if sides.index(longside) == 0: # width is longer
		im = im.resize((longsidemax, int(sides[1] / factor)), Image.ANTIALIAS)
		log(mode,"✅  " + root + '/' + filename + " was resized to " + str(longsidemax) + "x" + str(int(sides[1] / factor)) + " (" + str(percent) + " %).\n")
	if sides.index(longside) == 1: # height is longer
		im = im.resize((int(sides[0] / factor), longsidemax), Image.ANTIALIAS)
		log(mode,"✅  " + root + '/' + filename + " was resized to " + str(int(sides[0] / factor)) + "x" + str(longsidemax) + " (" + str(percent) + " %).\n")
	return im, percent

##############################################################################
# Analyze and resize all the Renderings
##############################################################################

print '💡  The fun can begin' + '...'
# check if small size was there before
if os.path.isdir(os.getcwd() + '/' + smallsizepath):
	log(mode,"❎  The folder " + smallsizepath + " already exists, deleting it…\n")
	shutil.rmtree(os.getcwd() + '/' + smallsizepath)

sourcefolder = os.getcwd() + '/' + fullsizepath
targetfolder = sourcefolder.replace(fullsizepath, smallsizepath)

# Copy the source folder and work on that material
shutil.copytree(sourcefolder, targetfolder, symlinks=False, ignore=None)

sublist = [sub for sub in os.listdir(targetfolder) if os.path.isdir(os.path.join(targetfolder,sub))]

for path in sublist:
	filecounter = 0
	lampfolder = targetfolder + '/' + path
	allFolderPositions, filelist, widths, heights = [], [], [], []
	spinner = MoonSpinner('⏳  .pngs 🖼  are being counted. ')
	for root, directories, filenames in os.walk(lampfolder):
		for filename in filenames:	
			if filename.lower().endswith('.png'):
				filecounter += 1
				spinner.next()
	spinner.finish()
	
	bar = ShadyBar('⏳  Resizing... ' + path + '\t', max=filecounter, width=60)	
	for root, directories, filenames in os.walk(lampfolder):
		for filename in filenames:	
			if filename.lower().endswith('.png'):
				im = Image.open(root + '/' + filename)
				im, percent = occ_resize_small(im, root, filename)
				im.save(root + '/' + filename)
				processcounter += 1
				if percent > 100:
					enlargecounter += 1
				if percent <= 100:
					reducecounter += 1
				bar.next()
	bar.finish()			
	log(mode, path + ' »»' + str(filecounter) + '.png files have been processed.\n')

log("print",'⏱  %s .png files were resized in %.2f seconds (%.2f files per second).\n' % (processcounter, (time.time() - start_time), filecounter/(time.time() - start_time)))
log("print",'🔼  %s .png were reduced in size, 🔽  %s where enlarged.\n' % (reducecounter, enlargecounter))
log("print",'❎  %s errors.' % (errorcounter))
exit()
