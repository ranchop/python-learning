import numpy as np
from scipy import optimize
import matplotlib.pyplot as pp


def fit_leastsq(function, guess, y, x = None):
    # If x in not provided, then create a default value
    if x is None: x = np.arange(y.shape[0])

    # Define fitting function to be minimized
    def fitfun(A): return y - function(A,x)

    # Create fit
    fitresult = optimize.leastsq(fitfun, guess, full_output = True)

    print('Fit results: ',fitresult[0])
    print('cov_x matrix:', fitresult[1])
    print('info dict: with several keys')
    print('Message:', fitresult[3])
    print('Flag, fit successful?:' , fitresult[4])

def curvefit(function, guess, y, x = None):
    # If x in not provided, then create a default value
    if x is None: x = np.arange(y.shape[0])

    # Fit
    fitresult, errors = optimize.curve_fit(function, x, y, guess)

    # Outputs
    


def main():
    
    # Fitting function
    def f(A, x): return A[0] * np.exp(- (x-A[1])**2 / (2*A[2]**2) )

    # Generate data and fit
    xi = -np.linspace(-4, 4, 100)
    data = f([3,1,1.3],xi) + np.random.normal(size = xi.shape, scale = 0.1)
    fit_leastsq(f,[3,1,1],data,xi)
    # [mu, sigma, height] = fit(f, [mu, sigma, height], data, xi)[0]
    # mu = Parameter(mu)
    # sigma = Parameter(sigma)
    # height = Parameter(height)
    # pp.plot(xi,data,'o')
    # pp.plot(xi,f(xi))
    # pp.show()
    # print(mu(),sigma(),height())


if __name__ == '__main__':
    main()