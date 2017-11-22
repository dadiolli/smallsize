# -*- coding: utf-8 -*-
##############################################################################
# Settings
##############################################################################

longsidemax = 1400
enlarge = False # use "True" to allow increase of image size
fullsizepath = 'full_size' # directory with full size images
smallsizepath = 'small' # target folder
mode = "log" # use print to see output on console as well.

##############################################################################
# Import some stuff
##############################################################################

import checksumdir, os, shutil, sys, time
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

def img_resize(im, root, filename):
	sides = [im.width, im.height]
	longside = max(sides) * 1.0
	factor = longside / longsidemax
	percent = round(1 / factor * 100,2)
	if longside > longsidemax or enlarge == True:		
		if sides.index(longside) == 0: # width is longer
			im = im.resize((longsidemax, int(sides[1] / factor)), Image.ANTIALIAS)
			log(mode,"✅  " + root + '/' + filename + " was resized to " + str(longsidemax) + "x" + str(int(sides[1] / factor)) + " (" + str(percent) + " %).\n")
		if sides.index(longside) == 1: # height is longer
			im = im.resize((int(sides[0] / factor), longsidemax), Image.ANTIALIAS)
			log(mode,"✅  " + root + '/' + filename + " was resized to " + str(int(sides[0] / factor)) + "x" + str(longsidemax) + " (" + str(percent) + " %).\n")
	else:
		log(mode,"❎  " + root + '/' + filename + " remained unchanged.\n")
	return im, percent

def dir_changed(directory):
	checksum = checksumdir.dirhash(directory, excluded_files=['checksum.txt'])
	try:
		with open(directory + '/' + 'checksum.txt', 'r') as checkfile:
			checksum_old = checkfile.read()
			if checksum == checksum_old:
				log("print", "⏭  " + directory + " has remained unchanged, skipping.")
				return False
			else:
				log("print", "📂  " + directory + " has been changed, processing...")
				with open (directory + '/' + 'checksum.txt', 'wb') as checkfile:
					checkfile.write(checksum)
				return True
	except:
		with open (directory + '/' + 'checksum.txt', 'wb') as checkfile:
			checkfile.write(checksum)
			log("print", "📂  " + directory + " hasn't been processed before.")
			return True

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
	process = dir_changed(sourcefolder + '/' + path)
	if process:
		allFolderPositions, filelist, widths, heights = [], [], [], []
		spinner = MoonSpinner('⏳  images 🖼  are being counted. ')
		for root, directories, filenames in os.walk(lampfolder):
			for filename in filenames:	
				if filename.lower().endswith('.png' or '.jpg'):
					filecounter += 1
					spinner.next()
		spinner.finish()
		
		bar = ShadyBar('⏳  Resizing... ' + path + '\t', max=filecounter, width=60)	
		for root, directories, filenames in os.walk(lampfolder):
			for filename in filenames:	
				if filename.lower().endswith('.png' or '.jpg'):
					im = Image.open(root + '/' + filename)
					im, percent = img_resize(im, root, filename)
					im.save(root + '/' + filename)
					processcounter += 1
					if percent > 100:
						enlargecounter += 1
					if percent <= 100 and enlarge == True:
						reducecounter += 1
					bar.next()
		bar.finish()			
	log(mode, path + ' »»' + str(filecounter) + 'image files have been processed.\n')

log("print",'⏱  %s image files were processed in %.2f seconds (%.2f files per second).' % (processcounter, (time.time() - start_time), filecounter/(time.time() - start_time)))
log("print",'🔼  %s images were enlarged size, 🔽  %s where reduced in size.' % (reducecounter, enlargecounter))
log("print",'❎  %s errors.' % (errorcounter))
exit()
