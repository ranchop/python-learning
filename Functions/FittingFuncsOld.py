import numpy as np
from scipy import optimize
import matplotlib.pyplot as pp

class Parameter:
    def __init__(self, value):
            self.value = value

    def set(self, value):
            self.value = value

    def __call__(self):
            return self.value

def fit(function, parameters, y, x = None):
    def f(params):
        i = 0
        for p in parameters:
            p.set(params[i])
            i += 1
        return y - function(x)

    if x is None: x = np.arange(y.shape[0])
    p = [param() for param in parameters]
    return optimize.leastsq(f, p)

def main():
    # Fitting parameters
    mu = Parameter(0)
    sigma = Parameter(1)
    height = Parameter(5)

    # Fitting function
    def f(x): return height() * np.exp(- (x-mu())**2 / (2*sigma()**2) )

    # Generate data and fit
    xi = -np.linspace(-4, 4, 100)
    data = f(xi) + np.random.normal(size = xi.shape, scale = 0.1)
    [mu, sigma, height] = fit(f, [mu, sigma, height], data, xi)[0]
    mu = Parameter(mu)
    sigma = Parameter(sigma)
    height = Parameter(height)
    pp.plot(xi,data,'o')
    pp.plot(xi,f(xi))
    pp.show()
    print(mu(),sigma(),height())


if __name__ == '__main__':
    main()