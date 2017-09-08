import numpy as np
import os
import datetime
import re
import pyfits
import matplotlib.pyplot as pp
from shutil import copyfile


# get path to store downloaded images
def backuploc():
	# Get user home directory
	basepath = os.path.expanduser('~')

	# Find out the os
	from sys import platform as _platform
	
	# Platform dependent storage
	if _platform == 'darwin': 
		# Mac OS X
		backuppath = os.path.join(basepath, 'Documents', 'My Programs', 'Raw Imagedata Temporary')
	elif _platform == 'win32' or _platform == 'cygwin': 
		# Windows
		backuppath = os.path.join(basepath, 'Documents', 'My Programs', 'Raw Imagedata Temporary')
	else:
		# Unknown platform
		return None

	# If the folder doesn't exist, create it
	if not(os.path.exists(backuppath)): os.makedirs(backuppath)

	return backuppath


# If the extension is not provided, add the default of .fits
def fixentension(filename):
	# Add the .fits extension if not present
	imageformat = os.path.splitext(filename)[1]
	if imageformat == '': filename += '.fits'
	return filename

# Copy image to local backup location
def backupimage(imagepath_original, imagepath_backup):
	backuppath = os.path.split(imagepath_backup)[0]
	if not(os.path.exists(backuppath)): os.makedirs(backuppath)
	copyfile(imagepath_original, imagepath_backup)


# string for subfolder = imagename2subfolder( string for image name )
def imagename2subfolder(imagename = None):
    # Special case if imagename is not provided
    if imagename is None: return 'None'
    
    # Default values for pattern (future version: include as an optional input)
    re_pattern = '\d\d-\d\d-\d\d\d\d_\d\d_\d\d_\d\d'
    datetime_format = '%m-%d-%Y_%H_%M_%S'
    
    # Find '/' in the string and remove it
    
    # Extract datetime
    imagetimestr = re.findall(re_pattern,imagename)
    if len(imagetimestr) == 1: imagetimestr = imagetimestr[0]
    else: return 'None'
    try: imagetime = datetime.datetime.strptime(imagetimestr,datetime_format)
    except ValueError as err: return err
    
    # Create subfolder
    imageyear = imagetime.strftime('%Y')
    imagemonth = imagetime.strftime('%Y-%m')
    imagedate = imagetime.strftime('%Y-%m-%d')
    subfolder = os.path.join( imageyear, imagemonth, imagedate )
    
    return subfolder


# imagedata = imagename2imagepath(imagename)
def imagename2imagepath(imagename):
	# Extract the subfolder path
	subpath = imagename2subfolder(imagename)

	# Fix the extension
	imagename = fixentension(imagename)

	# Check if it exists on temporary location
	imagepath_backup = os.path.join(backuploc(), subpath, imagename)
	if os.path.exists(imagepath_backup):
		return imagepath_backup

	# Find the base path depending on the platform
	from sys import platform as _platform
	if _platform == 'darwin': 
		# Mac OS X
		basepath = '/Volumes/Raw Data/Images'
	elif _platform == 'win32' or _platform == 'cygwin': 
		# Windows
		basepath = '\\\\18.62.1.253\\Raw Data\\Images'
	else:
		# Unknown platform
		basepath = None

	# Check if server is connected
	if os.path.exists(basepath) is False:
		raise FileNotFoundError('Server NOT connected!')

	# Find the fullpath to the image
	imagepath = os.path.join(basepath,subpath,imagename)

	# Check if file exists
	if os.path.exists(imagepath) is False:
		raise FileNotFoundError('Image NOT present on the server: Possibly invalid filename?')

	# Copy file to backup location
	backupimage(imagepath, imagepath_backup)

	return imagepath


# imagedata_raw = imagepath2imagedataraw(imagepath)
def imagepath2imagedataraw_fits(imagepath):
	# Check that imagepath is a valid path
	if os.path.exists(imagepath) is False: 
		print('Invalid Filepath')
		return []
	
	# Load fits file
	imagedata_raw = pyfits.open(imagepath)
	imagedata_raw = imagedata_raw[0].data

	return imagedata_raw

# imagedata_raw = imagepath2imagedataraw(imagepath)
def imagepath2imagedataraw(imagepath):
	# Find the image format 
	imageformat = os.path.splitext(imagepath)[1]

	if imageformat == '.fits':
		return imagepath2imagedataraw_fits(imagepath)
	else:
		print('Unknown file type')
		return None



# imagedata_od = imagedataraw2od(imagedata_raw)
def imagedataraw2od(imagedata_raw):
	# Check the dimension of the raw image
	if imagedata_raw.shape[0] == 3:
		imagedata_raw[0] -= imagedata_raw[2]
		imagedata_raw[1] -= imagedata_raw[2]
	elif imagedata_raw.shape[0] == 4:
		imagedata_raw[0] -= imagedata_raw[2]
		imagedata_raw[1] -= imagedata_raw[3]
	else:
		raise NotImplementedError('Not a valid absorbance image: doesn\'t have 3 or 4 images')

	# Calculate absorbance image
	absorbance = imagedata_raw[0] - imagedata_raw[1]

	# Calculate OD
	imagedata_od = np.log(imagedata_raw[1]/imagedata_raw[0])

	# Remove nan and inf with average of the surrounding

	# Return
	return imagedata_od

# Scale image without atoms to match with atoms
#def 


#
def imagename2od(imagename):
	imagepath = imagename2imagepath(imagename)
	imagedata_raw = imagepath2imagedataraw(imagepath)
	imagedata_od = imagedataraw2od(imagedata_raw)
	return imagedata_od



def main():
	### Run tests
	sample_imagename = '03-31-2016_19_39_09_top'

	
	subfolderstr = imagename2subfolder(sample_imagename)
	imagepath = imagename2imagepath(sample_imagename)
	imagedata_raw = imagepath2imagedataraw(imagepath)
	imagedata_od = imagedataraw2od(imagedata_raw)

	print('--------------------------------------------------------')
	print('Image name:',sample_imagename)
	print('Image path:',imagepath)
	print('Image shape:',imagedata_raw.shape)
	print('Image od:',type(imagedata_od),imagedata_od.shape, imagedata_od.dtype)
	print('--------------------------------------------------------')

	pp.imshow(imagedata_od)
	pp.show()


if __name__ == '__main__':
	main()

