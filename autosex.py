import os
from prog import *
from numpy import loadtxt

mdirec = main_directory()
direcs = directories()
img = rimage(direcs[0])
xg = []
if len(img) == 0: pass
else:
	try: 
		zps = loadtxt(mdirec+"/zps",dtype="str")
		c1 = True
	except IOError: 
		print "I did't find 'zps' file." 
		c1 = False 
	if c1 == True:
			os.chdir(direcs[0])
			rimg,wimg,o = have_weight_map(img)
			x = xgs(rimg,zps[:,0])
			if wimg != []:
				wimg = sort_wmap(rimg,wimg,x)
			else: pass
			hparam = header_param(rimg)
			zps = sort_zp(rimg,zps,x)
			os.chdir("..")
			running(direcs,rimg,hparam,wimg,zps,"Sloan_r",x)	
		
	else: print "I can't run... bye"	
		
			