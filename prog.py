def main_directory():
	import os
	global cdirec
	cdirec = os.getcwd()
	while True:
		c = 0
		mdirec = raw_input("Enter the main directory (enter or '.' for current directory): ")
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
		dimages = raw_input("Insert images directory: ")
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
		tosepar = raw_input("Insert images to run sextractor ('*' for every images)(enter to stop): ")
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

def rel_img_wmap(img,wim):
	import numpy as np
	import pyfits as pf
	wsort = np.zeros(len(img))
	wsort = list(wsort.astype("str"))

	for i in range(len(img)):
		im = pf.open(img[i])
		imx,imy = im[0].header["NAXIS1"],im[0].header["NAXIS2"]
		cand = []
		for j in wim:
			w = pf.open(j)
			wx,wy = w[0].header["NAXIS1"],w[0].header["NAXIS2"]
			if wx - imx == 0 and wy - imy == 0:
				cand = cand + [j]

		for p in range(len(wsort)):
			cond = np.array(cand) == wsort[p]
			c = np.where(cond == True)
			if len(c[0]) != 0:
				cand.remove(cand[int(c[0])])
			else: pass

		if len(cand) == 0: 
			print "Not found weight-map for "+img[i]+" image "
			wsort[i] = "NOIMAGE"
		elif len(cand) == 1:
			wsort[i] = cand[0]
		else:
			 
			x = 0
			while x != 1:
				print "*"*30
				print "I found "+str(len(cand))+" candidates for "+img[i]+" weight-map"
				print "They are: "
				for k in cand: print k
				cand1 = raw_input("Please, give me the weight-map name: ")
				for j in cand:
					if cand1 == j: 
						x = 1
				if x == 1: 
					wsort[i] = cand1
				else: print cand1+" isn't a candidate."
	return wsort 
def header_param(img):
	import pyfits as pf
	t,gain = [],[]
	for i in range(len(img)):
		im = pf.open(img[i])
		t,gain = t + [im[0].header["EXPTIME"]], gain + [im[0].header["GAIN"]]
	return [t,gain]
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

def read_zp(img):
	
    c = 0
    zps = []
    for i in img:
        while True:
            zp = raw_input("Insert zero-point magnitude for "+i+" image: ")
            try:
                zps = zps + [float(zp)]
                c = c + 1
                break
            except ValueError: print "ERROR: Zero-point magnitude has to be a number"
    return zps

def running(direc,img,hparam,wim,zps,nbase,x):
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
		os.system("sed 's/ZP/"+str(2.5*np.log10(hparam[0][i])+zps[0][i])+"/' pass2.sex > tpass2.sex; mv tpass2.sex pass2.sex") 
		os.system("sed 's/NGAIN/"+str(hparam[1][i])+"/' pass2.sex > tpass2.sex; mv tpass2.sex pass2.sex") 

		if img[i][x[i][0]:x[i][1]] == nbase:	
		        os.system("sex -c pass1.sex ../"+direc[0]+"/"+img[i])
		        os.system("psfex -c psfconf.c pass1.cat")
		        os.system("mv pass1.psf "+img[i][:-5]+".psf")
			os.system("sed 's/NPSF/"+img[i][:-5]+"/' pass2.sex > tpass2.sex; mv tpass2.sex pass2.sex")
			os.system("sex -c pass2.sex ../"+direc[0]+"/"+img[i])
		else: print "este no"
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
					os.system("sed 's/NWIMAGE1/"+wim[base]+"/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
					os.system("sed 's/IMGDIR/"+direc[0]+"/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
					os.system("sed 's/IMGDIR/"+direc[0]+"/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
					os.system("sed 's/NWIMAGE2/"+wim[i]+"/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
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
			os.system("sed 's/NPSF/"+img[i][:-5]+"/' conf_assoc.sex > t2.sex; mv t2.sex conf_assoc.sex")
			os.system("sex -c conf_assoc.sex ../"+direc[0]+"/"+img[base]+",../"+direc[0]+"/"+img[i])
	return True
	
#def match(img,nzp):
	#for i in range(len(nzp)):
		
	
	
	
			
def grafs_sep(catalog):
	import os
	import numpy as np
	import matplotlib.pyplot as plt
	os.system("mkdir -p "+catalog[:-4]+"_plots")
    
	cat = np.loadtxt(catalog)
	mkron,smodel,mu_max,flux_rad = cat[:,0],cat[:,9],cat[:,6],cat[:,8]
   	plt.figure() 
   	plt.scatter(mkron,smodel*10**2, s=0.5)
   	plt.xlabel(r"$magnitude_{kron} \ [mag]$")
   	plt.xlim(15,26)
   	plt.ylim(-1,5)
   	plt.ylabel(r"$[Spread \ Model]x10^{2}$")
   	plt.savefig("smodel_"+catalog[:-4])
   	os.system("mv smodel_"+catalog[:-4]+".png "+catalog[:-4]+"_plots")
    
   	plt.figure()
   	plt.scatter(mkron,mu_max, s=0.5)
   	plt.xlabel(r"$magnitude_{kron} \ [mag]$")
   	plt.xlim(15,26)
   	plt.ylim(15,26)
   	plt.ylabel(r"$\mu_{max}$")
   	plt.savefig("mumax_"+catalog[:-4])
   	os.system("mv mumax_"+catalog[:-4]+".png "+catalog[:-4]+"_plots")
   
   	plt.figure()
   	plt.scatter(mkron,flux_rad, s=0.5)
   	plt.xlim(15,26)
   	plt.ylim(1,20)
   	plt.xlabel(r"$magnitude_{kron} \ [mag]$")
   	plt.ylabel(r"$Half \ Flux \ Radius \ [pix]$")
   	plt.savefig("fluxrad_"+catalog[:-4])
   	os.system("mv fluxrad_"+catalog[:-4]+".png "+catalog[:-4]+"_plots")
   
   	os.chdir("..")
   	os.system("shotwell results_1/"+catalog[:-4]+"_plots/* &")

def graf_sim(images):
	import os
	import numpy as np
	import matplotlib.pyplot as plt
	os.system("mkdir -p sgsplots")
	for i in images:
		cat = np.loadtxt(i[:-5]+".cat")
		mkron,smodel,mu_max,flux_rad = cat[:,0],cat[:,7],cat[:,4],cat[:,6]
	plt.scatter(mkron,flux_rad, s=0.5)
	plt.xlim(15,26)
	plt.ylim(1,20)
	plt.xlabel(r"$magnitude_{kron} \ [mag]$")
	plt.ylabel(r"$Half \ Flux \ Radius \ [pixel]$")
	plt.savefig("flux_rad")
	os.system("mv flux_rad.png sgsplots")
	plt.figure()
	for i in images:
		cat = np.loadtxt(i[:-5]+".cat")
		mkron,smodel,mu_max,flux_rad = cat[:,0],cat[:,7],cat[:,4],cat[:,6]
		plt.scatter(mkron,smodel*10**2, s=0.5)
		plt.xlim(15,26)
		plt.ylim(-1,5)
		plt.xlabel(r"$magnitude_{kron} \ [mag]$")
		plt.ylabel(r"$Spread \ Model [x10^{2}] $")
	plt.savefig("smodel")
	os.system("mv smodel.png sgsplots")
	plt.figure()
	for i in images:
		cat = np.loadtxt(i[:-5]+".cat")
		mkron,smodel,mu_max,flux_rad = cat[:,0],cat[:,7],cat[:,4],cat[:,6]
		plt.scatter(mkron,mu_max, s=0.5)
	plt.xlim(15,26)
	plt.ylim(15,26)
	plt.xlabel(r"$magnitude_{kron} \ [mag]$")
	plt.ylabel(r"$\mu_{max} $")
	plt.savefig("mu_max")
	os.system("mv mu_max.png sgsplots")
	os.system("shotwell sgsplots/*.png &")
	os.chdir("..")

#mdirec = main_directory()
#direcs = directories()
#img = rimage(direcs[0])
#if len(img) == 0: pass
#else:
#    	os.chdir(direcs[0])
#    	rimg,wimg,o = have_weight_map(img)
#    	if o == True:
     		#wimg = rel_img_wmap(rimg,wimg)
#		wimg = sort_wmap(rimg,wimg,[11,18])
#    	else: print "You don't have weighting maps"
#    	hparam = header_param(rimg)
#	print hparam
#    	os.chdir("..")
#	zp = np.loadtxt("zps",dtype="str")
#	zps = sort_zp(rimg,zp,[11,18]) 
#	running(direcs,rimg,hparam,wimg,zps,"Sloan_r")
#	assoc(direcs,rimg,hparam,wimg,zps,"Sloan_r")
#    	for i in range(len(rimg)):
#        	grafs_sep(rimg[i][:-5]+".cat")

