# Default configuration file for PSFEx 3.17.1
# EB 2017-05-17
#
 
#-------------------------------- PSF model ----------------------------------
 
BASIS_TYPE      PIXEL_AUTO      # NONE, PIXEL, GAUSS-LAGUERRE or FILE
BASIS_NUMBER    20              # Basis number or parameter
BASIS_NAME      test.fits      # Basis filename (FITS data-cube)
BASIS_SCALE     1.0             # Gauss-Laguerre beta parameter
NEWBASIS_TYPE   NONE            # Create new basis: NONE, PCA_INDEPENDENT
                                # or PCA_COMMON
NEWBASIS_NUMBER 8               # Number of new basis vectors
PSF_SAMPLING    0.0             # Sampling step in pixel units (0.0 = auto)
PSF_PIXELSIZE   1.0             # Effective pixel size in pixel step units
PSF_ACCURACY    0.01            # Accuracy to expect from PSF "pixel" values
PSF_SIZE        25,25           # Image size of the PSF model
PSF_RECENTER    N               # Allow recentering of PSF-candidates Y/N ?
MEF_TYPE        INDEPENDENT     # INDEPENDENT or COMMON
 
#------------------------- Point source measurements -------------------------
 
CENTER_KEYS     X_IMAGE,Y_IMAGE # Catalogue parameters for source pre-centering
PHOTFLUX_KEY    FLUX_APER(1)    # Catalogue parameter for photometric norm.
PHOTFLUXERR_KEY FLUXERR_APER(1) # Catalogue parameter for photometric error
 
#----------------------------- PSF variability -------------------------------
 
PSFVAR_KEYS     X_IMAGE,Y_IMAGE # Catalogue or FITS (preceded by :) params
PSFVAR_GROUPS   1,1             # Group tag for each context key
PSFVAR_DEGREES  2               # Polynom degree for each group
PSFVAR_NSNAP    9               # Number of PSF snapshots per axis
HIDDENMEF_TYPE  COMMON          # INDEPENDENT or COMMON
STABILITY_TYPE  EXPOSURE        # EXPOSURE or SEQUENCE
 
#----------------------------- Sample selection ------------------------------
 
SAMPLE_AUTOSELECT  Y            # Automatically select the FWHM (Y/N) ?
SAMPLEVAR_TYPE     SEEING       # File-to-file PSF variability: NONE or SEEING
SAMPLE_FWHMRANGE   2.0,10.0     # Allowed FWHM range
SAMPLE_VARIABILITY 0.2          # Allowed FWHM variability (1.0 = 100%)
SAMPLE_MINSN       20           # Minimum S/N for a source to be used
SAMPLE_MAXELLIP    0.3          # Maximum (A-B)/(A+B) for a source to be used
SAMPLE_FLAGMASK    0x00fe       # Rejection mask on SExtractor FLAGS
SAMPLE_WFLAGMASK   0x0000       # Rejection mask on SExtractor FLAGS_WEIGHT
SAMPLE_IMAFLAGMASK 0x0          # Rejection mask on SExtractor IMAFLAGS_ISO
BADPIXEL_FILTER    N            # Filter bad-pixels in samples (Y/N) ?
BADPIXEL_NMAX      0            # Maximum number of bad pixels allowed
 
#----------------------- PSF homogeneisation kernel --------------------------

HOMOBASIS_TYPE     NONE         # NONE or GAUSS-LAGUERRE
HOMOBASIS_NUMBER   10           # Kernel basis number or parameter
HOMOBASIS_SCALE    1.0          # GAUSS-LAGUERRE beta parameter
HOMOPSF_PARAMS     2.0, 3.0     # Moffat parameters of the idealised PSF
HOMOKERNEL_DIR                  # Where to write kernels (empty=same as input)
HOMOKERNEL_SUFFIX  .homo.fits   # Filename extension for homogenisation kernels

#----------------------------- Output catalogs -------------------------------

OUTCAT_TYPE        NONE         # NONE, ASCII_HEAD, ASCII, FITS_LDAC
OUTCAT_NAME        psfex_out.cat  # Output catalog filename

#------------------------------- Check-plots ----------------------------------
 
CHECKPLOT_DEV       PS         # NULL, XWIN, TK, PS, PSC, XFIG, PNG,
                                # JPEG, AQT, PDF or SVG
CHECKPLOT_RES       0           # Check-plot resolution (0 = default)
CHECKPLOT_ANTIALIAS Y           # Anti-aliasing using convert (Y/N) ?
CHECKPLOT_TYPE      FWHM,ELLIPTICITY,COUNTS, COUNT_FRACTION, CHI2, RESIDUALS
                                # or NONE
CHECKPLOT_NAME      fwhm, ellipticity, counts, countfrac, chi2, resi
 
#------------------------------ Check-Images ---------------------------------
 
CHECKIMAGE_TYPE CHI,PROTOTYPES,SAMPLES,RESIDUALS,SNAPSHOTS
                                # or MOFFAT,-MOFFAT,-SYMMETRICAL
CHECKIMAGE_NAME chi.fits,proto.fits,samp.fits,resi.fits,snap.fits
                                # Check-image filenames
CHECKIMAGE_CUBE N               # Save check-images as datacubes (Y/N) ?
 
#----------------------------- Miscellaneous ---------------------------------
 
PSF_DIR                         # Where to write PSFs (empty=same as input)
PSF_SUFFIX      .psf            # Filename extension for output PSF filename
VERBOSE_TYPE    NORMAL          # can be QUIET,NORMAL,LOG or FULL
WRITE_XML       Y               # Write XML file (Y/N)?
XML_NAME        psfex.xml       # Filename for XML output
XSL_URL         file:///usr/local/share/psfex/psfex.xsl
                                # Filename for XSL style-sheet
NTHREADS        0               # Number of simultaneous threads for
                                # the SMP version of PSFEx
                                # 0 = automatic
 
