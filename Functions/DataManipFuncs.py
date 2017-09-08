

# Library of functions for common data manipulation

# Import libraries
import numpy as np
import matplotlib.pyplot as pp

def binPoints(*args, **kwargs):
	# Process inputs
	binsize = kwargs.get('binsize',2)

	# Calculate the size of binned data
	binDataSize = int(len(args[0])/binsize)

	# Create empty list for storing the results
	results = [None] * len(args)
	for j,arg in enumerate(args):
		results[j] = np.zeros(binDataSize)

	# Bin the data
	for i in range(binDataSize):
		for j,arg in enumerate(args):
			results[j][i] = np.mean(arg[i*binsize:(i+1)*binsize])

	# Return the results
	return results

def binX(x, *args, **kwargs):
	# Process inputs
	bins = kwargs.get('bins',50)
	edges = kwargs.get('edges',None)

	# Create empty list for storing the results
	

def main():
	##### Testing binPoints
	# Generate data
	x = np.linspace(-5,5,498)
	y1 = np.sin(3*x) - np.cos(x)
	y2 = np.sin(x**2) - np.log(np.abs(x))
	y1 = y1 + np.random.normal(0.0, 0.3, y1.shape )
	y2 = y2 + np.random.normal(0.0, 0.3, y2.shape )

	# Test function calls
	binsize = 5;
	[x_bin, y1_bin, y2_bin] = binPoints(x, y1, y2, binsize=binsize)
	print('Initial size of data: {} and binned (by {}) size: {}'.format(x.size, binsize, x_bin.size))
	pp.plot(x,y1,x,y2,x_bin,y1_bin,'.',x_bin,y2_bin,'.')
	pp.show()

	# Other ways to make function call
	[x_bin] = binPoints(x) # this will bin x by default binsize of 2, one can also pass in multiple arrays
	print('Binning a single Array with default values, initial size {} and final size {}'.format(x.size,x_bin.size))


if __name__ == '__main__':
	main()
