import os
import numpy as np
import matplotlib.pyplot as plt
import pyfits as pf

def main_directory():
	global cdirec
	cdirec = os.getcwd()
	while True:
		c,d = 0,0
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
						if inspec(i,"sex") == True and inspec(i,"param") == True:
							d = d + 1
					except OSError: pass

				if c > 0 and d > 0: return mdirec
				else: print "ERROR: Your main directory has to contain the image directory and configuration directory"
			else: print "ERROR: The directory "+mdirec+" is empty. "
			os.chdir(cdirec)
		except OSError: print("ERROR: No such directory "+mdirec)

def in_main(direc):
	x = 0
	ls = os.listdir(".")
	for i in ls:
		if i == direc: x = 1
	if x == 1: return True
	else: 
		print "ERROR: "+direc+" directory isn't in the main directory."
		return False

def inspec(direc,sub,*p):
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

def directories():
	while True:
		dimages = raw_input("Insert images directory: ")
		if in_main(dimages) == True:
			if inspec(dimages,"fits","yes") == True: break
			else: pass
	while True:
		dconf = raw_input("Insert configuration directory: ")
		if in_main(dconf) == True:
			if inspec(dconf,"sex","yes") == True and inspec(dconf,"param","yes") == True: break
			else: pass
	return [dimages,dconf]

def rimage(dimages):
	im = []
	images = os.listdir(dimages)
	print "*"*10+"files in "+dimages+" directory"+"*"*10
	for i in images: print i
	while True:
		x = 0
		images = os.listdir(dimages)
		tosepar = raw_input("Insert images to separate stars and galaxies ('*' for every images)(enter to stop): ")
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
				print("No images to separate")
				return im
			else: return im

def have_weight_map(img):
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
	t,gain = [],[]
	for i in range(len(img)):
		im = pf.open(img[i])
		t,gain = t + [im[0].header["EXPTIME"]], gain + [im[0].header["GAIN"]]
	return [t,gain]
def f_in_img(nimg,nfilter):
	for i in range(len(nimg)-len(nfilter)):
		if nfilter == nimg[i:i+len(nfilter)]: return [i,i+len(nfilter)]

def sort_zp(img,zps,x): 
	zp_sort,nzps = [],[]
	for i in img:
		for j in range(len(zps)):
			if i[x[0]:x[1]] == zps[j,0]: 
				zp_sort = zp_sort + [float(zps[j,1])]
				nzps = nzps + [zps[j,0]]
	return [zp_sort,nzps]

def sort_wmap(img,wim,x): 
	wmap_sort = []
	for i in img:
		for j in wim:
			if i[x[0]:x[1]] == j[x[0]:x[1]] : wmap_sort = wmap_sort + [j]
	return wmap_sort
		
	
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

def running(direc,img,hparam,wim,zps,nbase):
	os.system("mkdir -p results")
    	os.chdir("results")
    	for i in range(len(img)):
        	os.system("cp ../"+direc[1]+"/pass* .; mv pass_2.sex pass2.sex") #borrar despues
        	os.system("cp ../"+direc[1]+"/psf* . ")
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


		if img[i][11:18] == nbase:	
        		os.system("sex -c pass1.sex ../"+direc[0]+"/"+img[i])
        		os.system("psfex -c psfconf.c pass1.cat")
			os.system("mv pass1.psf "+img[i][:-5]+".psf")
			os.system("sed 's/NPSF/"+img[i][:-5]+"/' pass2.sex > tpass2.sex; mv tpass2.sex pass2.sex")
        		os.system("sex -c pass2.sex ../"+direc[0]+"/"+img[i])
		else: pass
    	os.chdir("..")
def nbase(nzps,nbase):
	c,x = 0,-1	
	for i in nzps:
		if i == nbase: x = c
		else: c = c + 1
	if x != -1: return x
	else: return False

def assoc(direc,img,hparam,wim,zps,nbase):
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
			if i != base:
				os.system("cp ../conf/*c*a* . ; mv conf_a.sex conf_assoc.sex") #borrar despues
                		if len(wim) != 0:
                        		if wim[i] !=  "NOIMAGE":
                               			os.system("sed 's/WNONE/MAP_WEIGHT/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
                                		os.system("sed 's/NWIMAGE1/"+wim[base]+"/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
                                		os.system("sed 's/IMGDIR/"+direc[0]+"/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
                                		os.system("sed 's/IMGDIR/"+direc[0]+"/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
                                		os.system("sed 's/NWIMAGE2/"+wim[i]+"/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
                        		else: os.system("sed 's/WNONE/NONE/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
                		else: os.system("sed 's/WNONE/NONE/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
                		os.system("sed 's/NGAIN/"+str(hparam[1][i])+"/' conf_assoc.sex > tc.sex; mv tc.sex conf_assoc.sex")
				os.system("sed 's/BASECAT/"+img[base][:-5]+".cat"+"/' conf_assoc.sex > tconf_assoc.sex; mv tconf_assoc.sex conf_assoc.sex")
                		os.system("sed 's/TEST/"+img[i][:-5]+"/' conf_assoc.sex > t2.sex; mv t2.sex conf_assoc.sex")
                		os.system("sed 's/NZP/"+zps[1][i]+"/' conf_assoc.sex > t2.sex; mv t2.sex conf_assoc.sex")
                		os.system("sed 's/ZP/"+str(2.5*np.log10(hparam[0][i])+zps[0][i])+"/' conf_assoc.sex > t2.sex; mv t2.sex conf_assoc.sex")
                		os.system("sed 's/NGAIN/"+str(hparam[1][i])+"/' conf_assoc.sex > t2.sex; mv t2.sex conf_assoc.sex")
				os.system("sed 's/NPSF/"+img[i][:-5]+"/' conf_assoc.sex > t2.sex; mv t2.sex conf_assoc.sex")
				os.system("sex -c conf_assoc.sex ../"+direc[0]+"/"+img[i]+" , ../"+direc[0]+"/"+img[base])
		return True
		
#def match(img,nzp):
	#for i in range(len(nzp)):
		
	
	
	
			
def grafs_sep(catalog):
	os.chdir("results_1")
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

mdirec = main_directory()
direcs = directories()
img = rimage(direcs[0])
if len(img) == 0: pass
else:
    	os.chdir(direcs[0])
    	rimg,wimg,o = have_weight_map(img)
    	if o == True:
     		#wimg = rel_img_wmap(rimg,wimg)
		wimg = sort_wmap(rimg,wimg,[11,18])
    	else: print "You don't have weighting maps"
    	hparam = header_param(rimg)
	print hparam
    	os.chdir("..")
	zp = np.loadtxt("zps",dtype="str")
	zps = sort_zp(rimg,zp,[11,18]) 
	running(direcs,rimg,hparam,wimg,zps,"Sloan_r")
	assoc(direcs,rimg,hparam,wimg,zps,"Sloan_r")
#    	for i in range(len(rimg)):
#        	grafs_sep(rimg[i][:-5]+".cat")

