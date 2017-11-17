def main_directory():
	import os
	global cdirec
	cdirec = os.getcwd()
	while True:
		c = 0
		mdirec = raw_input("Insert the main directory (enter or '.' for current directory): ")
		if mdirec == "": mdirec = cdirec
		try:
			f = os.listdir(mdirec)
			os.chdir(mdirec)
			if len(f) != 0: 
				for i in f:
					try: 
						if inspec(i,"fits") == True:
							c = c + 1
					except OSError: pass

				if c > 0: return mdirec
				else: print "ERROR: Your main directory has to contain the image directory and configuration directory"
			else: print "ERROR: The directory "+mdirec+" is empty. "
			os.chdir(cdirec)
		except OSError: print("ERROR: No such directory "+mdirec)

def in_main(direc):
	import os
	x = 0
	ls = os.listdir(".")
	for i in ls:
		if i == direc: x = 1
	if x == 1: return True
	else: 
		print "ERROR: "+direc+" directory isn't in the main directory."
		return False

def inspec(direc,sub,*p):
	import os 
	files = os.listdir(direc)
	l = []
	c = 0
	for i in files:
		subc = i[-1*len(sub):]
		if subc == sub: 
			c = c + 1
		else: l = l + [i]
	if c == 0: 
		if not p:
			return False
		else:
			print("ERROR: No "+"."+sub+" images in "+direc)
			return False
	else: return True

def directories(direc):
	import os
	dconf = os.getenv("AUTOSEXPATH")+"/conf"	
        f = os.listdir(direc)
        print "*"*10 + "files in the main directory "+"*"*10
        for i in f: print i
	while True:
		dimages = raw_input("Insert image directory: ")
		if in_main(dimages) == True:
			if inspec(dimages,"fits","yes") == True: break
			else: pass
	while True:
		if inspec(dconf,"sex","yes") == True and inspec(dconf,"param","yes") == True: break
		else: return False
	return [dimages,dconf]

def rimage(dimages):
	import os
	im = []
	images = os.listdir(dimages)
	print "*"*10+"files in "+dimages+" directory"+"*"*10
	for i in images: print i
	while True:
		x = 0
		images = os.listdir(dimages)
		tosepar = raw_input("Input images ('*' for every images): ")
		if tosepar == "*": 
			for i in images:
				if i[-4:] == "fits": im = im + [i]
			return im
		if tosepar != "":
			for i in images:
				if i == tosepar and tosepar[-4:] == "fits": 
					x = 1
			if x == 1: 
				im = im + [tosepar]
			else: print("ERROR: No "+tosepar+" image in "+dimages+" directory")
		else: 
			if len(im) == 0: 
				print("No images to run")
				return im
			else: return im

def have_weight_map(img):
	import numpy as np
	import pyfits as pf 
	img = np.array(img)
	rimg = list()
	wim = []
	for i in range(len(img)):
		a = pf.open(img[i])
		gain,exptime = a[0].header["GAIN"],a[0].header["EXPTIME"]
		if gain == 0 or exptime == 0: wim = wim + [img[i]]
		else: rimg = rimg + [img[i]]
	if len(wim) == 0: 
		print "You don't have weighting map images in images list"
		o = False
	else: o = True
	return [rimg,wim,o]

def header_param(img):
	import pyfits as pf
	t,gain,seeng,s_img = [],[],[],[]
	for i in range(len(img)):
		im = pf.open(img[i])
		t,gain,seeng,s_img = t + [im[0].header["EXPTIME"]], gain + [im[0].header["GAIN"]], seeng + [im[0].header["FWHM"]], s_img + [im[0].header["FWHM_IMG"]]
	return [t,gain,seeng,s_img]
def f_in_img(nimg,nfilter):
	a = "p"
	for i in range(len(nimg)-len(nfilter)):
		if nfilter == nimg[i:i+len(nfilter)]: 
			a = [i,i+len(nfilter)]
	return a

def sort_zp(img,zps,x): 
	zp_sort,nzps = [],[]
	for i in range(len(img)):
		for j in range(len(zps)):
			if img[i][x[i][0]:x[i][1]] == zps[j,0]: 
				zp_sort = zp_sort + [float(zps[j,1])]
				nzps = nzps + [zps[j,0]]
	return [zp_sort,nzps]
def xgs(img,nfilter):
	x = []
	for i in img:
		for j in nfilter:
			if f_in_img(i,j) != "p": 
				x = x + [f_in_img(i,j)]
	return x

def sort_wmap(img,wim,x): 
	if len(img) == len(wim):
		wmap_sort = []
		for i in range(len(img)):
			for j in wim:
				if img[i][x[i][0]:x[i][1]] == j[x[i][0]:x[i][1]] : wmap_sort = wmap_sort + [j]
		return wmap_sort
	else: return []

def running(direc,img,hparam,wim,zps,x):
	import os
	import numpy as np
	os.system("mkdir -p Results")
  	os.chdir("Results")
   	for i in range(len(img)):
		os.system("cp "+direc[1]+"/pass* .") 
		os.system("cp "+direc[1]+"/psf* . ")
		if len(wim) != 0:
	   		if wim[i] !=  "NOIMAGE":
				os.system("sed 's/WNONE/MAP_WEIGHT/' pass1.sex > tpass1.sex; mv tpass1.sex pass1.sex") 
				os.system("sed 's/WNONE/MAP_WEIGHT/' pass2.sex > tpass2.sex; mv tpass2.sex pass2.sex") 
				os.system("sed 's/NWIMAGE/"+wim[i]+"/' pass1.sex > tpass1.sex; mv tpass1.sex pass1.sex") 
				os.system("sed 's/IMGDIR/"+direc[0]+"/' pass1.sex > tpass1.sex; mv tpass1.sex pass1.sex") 
				os.system("sed 's/NWIMAGE/"+wim[i]+"/' pass2.sex > tpass2.sex; mv tpass2.sex pass2.sex") 
				os.system("sed 's/IMGDIR/"+direc[0]+"/' pass2.sex > tpass2.sex; mv tpass2.sex pass2.sex") 
			else: 
				os.system("sed 's/WNONE/NONE/' pass1.sex > tpass1.sex; mv tpass1.sex pass1.sex") 
				os.system("sed 's/WNONE/NONE/' pass2.sex > tpass2.sex; mv tpass2.sex pass2.sex") 
		else: 
			os.system("sed 's/WNONE/NONE/' pass1.sex > tpass1.sex; mv tpass1.sex pass1.sex") 
			os.system("sed 's/WNONE/NONE/' pass2.sex > tpass2.sex; mv tpass2.sex pass2.sex") 
		os.system("sed 's/NGAIN/"+str(hparam[1][i])+"/' pass1.sex > tpass1.sex; mv tpass1.sex pass1.sex") 
		os.system("sed 's/TEST/"+img[i][:-5]+"/' pass2.sex > tpass2.sex; mv tpass2.sex pass2.sex") 
		os.system("sed 's/TEST/"+img[i][:-5]+"/' pass1.sex > tpass1.sex; mv tpass1.sex pass1.sex") 
		os.system("sed 's/ZP/"+str(2.5*np.log10(hparam[0][i])+zps[0][i])+"/' pass2.sex > tpass2.sex; mv tpass2.sex pass2.sex") 
		os.system("sed 's/NGAIN/"+str(hparam[1][i])+"/' pass2.sex > tpass2.sex; mv tpass2.sex pass2.sex")
		os.system("sed 's/FWHMARC/"+str(hparam[2][i])+"/' pass1.sex > tpass1.sex; mv tpass1.sex pass1.sex")
		os.system("sed 's/FWHMARC/"+str(hparam[2][i])+"/' pass2.sex > tpass2.sex; mv tpass2.sex pass2.sex")
		os.system("sed 's/APERPHOT/"+str(3*float(hparam[3][i]))+"/' pass1.sex > tpass1.sex; mv tpass1.sex pass1.sex")
		os.system("sed 's/APERPHOT/"+str(3*float(hparam[3][i]))+"/' pass2.sex > tpass2.sex; mv tpass2.sex pass2.sex") 
 

		
	
		        
		os.system("sex -c pass1.sex ../"+direc[0]+"/"+img[i])
		os.system("sed 's/TEST/"+img[i][:-5]+"/' psfconf.c > tpsf.c; mv tpsf.c psfconf.c") 
	        os.system("psfex -c psfconf.c "+img[i][:-5]+".cat")
		os.system("sed 's/NPSF/"+img[i][:-5]+"/' pass2.sex > tpass2.sex; mv tpass2.sex pass2.sex")
	os.chdir("..")

def nbase(nzps,nbase):
	c,x = 0,-1	
	for i in nzps:
		if i == nbase: x = c
		else: c = c + 1
	if x != -1: return x
	else: return False

def assoc(direc,img,hparam,wim,zps,nbase):
	import numpy as np
	import os
	c,x = 0,-1	
	for i in zps[1]:
		if i == nbase: x = c
		else: c = c + 1
	if x == -1: return False	
	else: 
		base = x
		os.system("mkdir -p Assoc")
		os.chdir("Assoc")
		for i in range(len(img)):
			os.system("cp "+direc[1]+"/*assoc* . ") 
			if len(wim) != 0:
				if wim[i] !=  "NOIMAGE":
					os.system("sed 's/WNONE/MAP_WEIGHT/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
					os.system("sed 's/NWIMAGE1/"+wim[i]+"/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
					os.system("sed 's/IMGDIR/"+direc[0]+"/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
				else: 
					os.system("sed 's/WNONE/NONE/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
			else: 
				os.system("sed 's/WNONE/NONE/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
			os.system("sed 's/NGAIN/"+str(hparam[1][i])+"/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
			os.system("sed 's/BASECAT/"+img[base][:-5]+".cat"+"/' conf_assoc.sex > tconf_assoc.sex; mv tconf_assoc.sex conf_assoc.sex")
			os.system("sed 's/TEST/"+img[i][:-5]+"/' conf_assoc.sex > t2.sex; mv t2.sex conf_assoc.sex")
			os.system("sed 's/NZP/"+zps[1][i]+"/' conf_assoc.sex > t2.sex; mv t2.sex conf_assoc.sex")
			os.system("sed 's/ZP/"+str(2.5*np.log10(hparam[0][i])+zps[0][i])+"/' conf_assoc.sex > t2.sex; mv t2.sex conf_assoc.sex")
			os.system("sed 's/NGAIN/"+str(hparam[1][i])+"/' conf_assoc.sex > t2.sex; mv t2.sex conf_assoc.sex")
			os.system("sed 's/FWHMARC/"+str(hparam[2][i])+"/' conf_assoc.sex > t2.sex; mv t2.sex conf_assoc.sex")
			os.system("sed 's/APERPHOT/"+str(3*float(hparam[3][i]))+"/' conf_assoc.sex > t2.sex; mv t2.sex conf_assoc.sex")
			os.system("sed 's/NPSF/"+img[i][:-5]+"/' conf_assoc.sex > t2.sex; mv t2.sex conf_assoc.sex")
			os.system("sex -c conf_assoc.sex ../"+direc[0]+"/"+img[base]+",../"+direc[0]+"/"+img[i])
	return True
	
