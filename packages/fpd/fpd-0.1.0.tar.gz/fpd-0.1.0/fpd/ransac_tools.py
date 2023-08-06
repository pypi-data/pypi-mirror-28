from skimage.measure.fit import BaseModel
from skimage.measure import ransac
import scipy as sp
import numpy as np


class _Plane3dModel(BaseModel):
    """Total least squares estimator for plane fit to 3-D point cloud.
    
    Attributes
    ----------
    model_data : array
        Fitted model.
    params : array
        model = C[0]*x + C[1]*y + C[2]
     
    """
    
    def my_model(self, p, *args):
        (x, y, z) = args
        m = p[0]*x + p[1]*y + p[2]
        return m
    
    def estimate(self, data):
        """Estimate model from data.
        
        Parameters
        ----------
        data : (N, D) array
            Flattened length N (x,y,z) point cloud to fit to.
        
        Returns
        -------
        success : bool
            True, if model estimation succeeds.
        """
        
        if False:
            return False
        else:
            # best-fit linear plane
            # https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.linalg.lstsq.html
            x, y, z = data.T
            A = np.c_[x, y, np.ones(data.shape[0])]
            C,_,_,_ = sp.linalg.lstsq(A, z)    # coefficients
            
            self.params = C
            return True


    def residuals(self, data):
        """Determine residuals of data to model.
        
        Parameters
        ----------
        data : (N, D) array
            Flattened length N (x,y,z) point cloud to fit to.
            
        Returns
        -------
        residuals : (N) array
            Z residual for each data point. 
             
        """
        
        x, y, z = data.T
        C = self.params
        # evaluate model at points
        args = (x, y, z)
        model = self.my_model(self.params, *args)
        
        #model = C[0]*x + C[1]*y + C[2]
        self.model_data = model
        z_error = model - z
        return z_error


class _Poly3dModel(BaseModel):
    """Total least squares estimator for quadratic fit to 3-D point cloud.
    
    Attributes
    ----------
    model_data : array
        Fitted model.
    params : array
        Model params.
    
    Notes
    -----
    Quadratic equation based on:
    https://stackoverflow.com/questions/18552011/3d-curvefitting/18648210#18648210.
    
    """

    def my_model(self, p, *args):
        (x, y, z) = args
        m = np.dot(np.c_[np.ones(x.shape), x, y, x*y, x**2, y**2], p)
        return m
    
    
    def estimate(self, data):
        """Estimate model from data.
        
        Parameters
        ----------
        data : (N, D) array
            Flattened length N (x,y,z) point cloud to fit to.
        
        Returns
        -------
        success : bool
            True, if model estimation succeeds.
        """
        
        if False:
            return False
        else:
            # best-fit quadratic curve
            A = np.c_[np.ones(data.shape[0]), data[:,:2], 
                      np.prod(data[:,:2], axis=1), data[:,:2]**2]
            C,_,_,_ = sp.linalg.lstsq(A, data[:,2])
            self.params = C
            return True
        

    def residuals(self, data):
        """Determine residuals of data to model.
        
        Parameters
        ----------
        data : (N, D) array
            Flattened length N (x,y,z) point cloud to fit to.
            
        Returns
        -------
        residuals : (N) array.
            Z residual for each data point.
        """
        
        x, y, z = data.T
        C = self.params
        # evaluate model at points
        args = (x, y, z)
        model = self.my_model(self.params, *args)
        
        #model = np.dot(np.c_[np.ones(x.shape), x, y, x*y, x**2, y**2], C)
        self.model_data = model
        z_error = model - z
        return z_error


class _Poly3dParaboloidModel(BaseModel):
    """Total least squares estimator for paraboloid fit to 3-D point cloud.
    
    Attributes
    ----------
    model_data : array
        Fitted model.
    params : array
        Model params.
        
    """
    
    
    def my_model(self, p, *args):
        (x, y, z) = args
        m = np.abs(p[0])*((x-p[1])**2 + (y-p[2])**2) + p[3]
        return m
    
    def my_dfun(self, p, *args):
        (x, y, z) = args
        da = ((x-p[1])**2 + (y-p[2])**2)
        dx = -2*np.abs(p[0])*(x-p[1])
        dy = -2*np.abs(p[0])*(y-p[2])
        dc = np.ones(dy.shape[0])
        return np.array([da, dx, dy, dc])
    
    def my_fit(self, p, *args):
        m = self.my_model(p, *args)
        (x, y, z) = args
        return m - z
    
    
    def estimate(self, data):
        """Estimate model from data.
        
        Parameters
        ----------
        data : (N, D) array
            Flattened length N (x,y,z) point cloud to fit to.
        
        Returns
        -------
        success : bool
            True, if model estimation succeeds.
        """
        
        # checks for validity of selected data would go here
        if False:
            return False
        else:
            x, y, z = data.T
            p0 = (0.1, x.mean(), y.mean(), 0)
            args = (x, y, z)
            popt, ier = sp.optimize.leastsq(func=self.my_fit, x0=p0, args=args,
                                            maxfev=10000, full_output=False,
                                            Dfun=self.my_dfun, col_deriv=True)
            self.params = popt
            if ier > 4:
                return False
            else:
                return True
        
    
    def residuals(self, data):
        """Determine residuals of data to model.
        
        Parameters
        ----------
        data : (N, D) array
            Flattened length N (x,y,z) point cloud to fit to.
            
        Returns
        -------
        residuals : (N) array
            Z residual for each data point.
        """
        
        x, y, z = data.T
        C = self.params
        
        # evaluate model at points       
        args = (x, y, z)
        m = self.my_model(self.params, *args)
        self.model_data = m
        z_error = m - z
        return z_error


def _model_class_gen(model_f, p0):   
    class FuncModel(BaseModel):
        """Total least squares estimator for paraboloid fit to 3-D point cloud.
        
        Attributes
        ----------
        model_data : array
            Fitted model.
        params : array
            Model params.
            
        """       
        
        def my_model(self, p, *args):
            m = model_f(p, *args) 
            return m
        
        def my_fit(self, p, *args):
            m = self.my_model(p, *args)
            (x, y, z) = args
            return m - z
        
        def p0_f(self):
            # probably is a cleaner way than function for storing p0.
            return p0
        
        
        def estimate(self, data):
            """Estimate model from data.
            
            Parameters
            ----------
            data : (N, D) array
                Flattened length N (x,y,z) point cloud to fit to.
            
            Returns
            -------
            success : bool
                True, if model estimation succeeds.
            """
            
            # checks for validity of selected data would go here
            if False:
                return False
            else:
                x, y, z = data.T
                p0 = self.p0_f()
                args = (x, y, z)
                popt, ier = sp.optimize.leastsq(func=self.my_fit, x0=p0, 
                                                args=args, maxfev=10000,
                                                full_output=False)
                self.params = popt
                if ier > 4:
                    return False
                else:
                    return True
            
        
        def residuals(self, data):
            """Determine residuals of data to model.
            
            Parameters
            ----------
            data : (N, D) array
                Flattened length N (x,y,z) point cloud to fit to.
                
            Returns
            -------
            residuals : (N) array
                Z residual for each data point.
            """
            
            x, y, z = data.T
            C = self.params
            
            # evaluate model at points       
            args = (x, y, z)
            m = self.my_model(self.params, *args)
            self.model_data = m
            z_error = m - z
            return z_error

    return FuncModel


def ransac_im_fit(im, mode=1, residual_threshold=0.1, min_samples=10, 
                  max_trials=1000, model_f=None, p0=None, mask=None, 
                  scale=False, fract=1):
    '''
    Fits a plane, polynomial, convex paraboloid, or arbirary function
    to an image using the RANSAC algorithm.
    
    Parameters
    ----------
    im : ndarray
        2-D image to fit to.
    mode : integer [1:3]
        Specifies model used for fit.
        0 is function defined by `model_f`.
        1 is plane.
        2 is quadratic.
        3 is concave paraboloid with offset.
    model_f : callable or None
        Function to be fitted.
        Definition is model_f(p, *args), where p is 1-D iterable of params
        and args is iterable of (x, y, z) arrays of point cloud coordinates.  
        See examples.
    p0 : tuple
        Initial guess of fit params for `model_f`.
    mask : 2-D boolean array
        Array with which to mask data. True values are ignored.
    scale : bool
        If True, `residual_threshold` is scaled by stdev of `im`.
    fract : scalar (0, 1]
        Fraction of data used for fitting, chosen randomly. Non-used data 
        locations are set as nans in `inliers`. 
        
    
    RANSAC Parameters
    -----------------
    residual_threshold : float
        Maximum distance for a data point to be classified as an inlier.
    min_samples : int
        The minimum number of data points to fit a model to.
    max_trials : int, optional
        Maximum number of iterations for random sample selection.
        
    Returns
    -------
    Tuple of fit, inliers, n, where:
    fit : 2-D array
        Image of fitted model.
    inliers : 2-D array
        Boolean array describing inliers.
    n : array or None
        Normal of plane fit. `None` for other models.
    
    Notes
    -----
    See skimage.measure.ransac for details of RANSAC algorithm.
    
    `min_samples` should be chosen appropriate to the size of the image
    and to the variation in the image.
    
    Increasing `residual_threshold` increases the fraction of the image
    fitted to.
    
    
    Examples
    --------
    `model_f` for paraboloid with offset:
    
    >>> def model_f(p, *args):
    ...     (x, y, z) = args
    ...     m = np.abs(p[0])*((x-p[1])**2 + (y-p[2])**2) + p[3]
    ...     return m
    >>> p0 = (0.1, 10, 20, 0)


    To plot fit, inliers etc:
    
    >>> from fpd.ransac_tools import ransac_im_fit
    >>> import matplotlib as mpl
    >>> from numpy.ma import masked_where
    >>> import numpy as np
    >>> import matplotlib.pylab as plt
    >>> plt.ion()
    
    
    >>> cmap = mpl.cm.gray
    >>> cmap.set_bad('r')
    
    >>> image = np.random.rand(*(64,)*2)
    >>> fit, inliers, n = ransac_im_fit(image, mode=1)
    >>> cor_im = image-fit
    >>> 
    >>> pct = 0.5
    >>> vmin, vmax = np.percentile(cor_im, [pct, 100-pct])
    >>> 
    >>> im = plt.matshow(masked_where(inliers==False, fit), cmap=cmap)
    >>> im = plt.matshow(masked_where(inliers==False, image), cmap=cmap)
    >>> im = plt.matshow(cor_im, vmin=vmin, vmax=vmax)
    
    
    To plot plane normal vs threshold:
    
    >>> from fpd.ransac_tools import ransac_im_fit
    >>> from numpy.ma import masked_where
    >>> import numpy as np
    >>> from tqdm import tqdm
    >>> import matplotlib.pylab as plt
    >>> plt.ion()
    
    >>> image = np.random.rand(*(64,)*2)
    >>> ns = []
    >>> rts = np.logspace(0, 1.5, 5)
    >>> for rt in tqdm(rts):
    ...     nis = []
    ...     for i in range(64):
    ...         fit, inliers, n = ransac_im_fit(image, residual_threshold=rt, max_trials=10)
    ...         nis.append(n)
    ...     ns.append(np.array(nis).mean(0))
    >>> ns = np.array(ns)
    
    >>> thx = np.arctan2(ns[:,1], ns[:,2])
    >>> thy = np.arctan2(ns[:,0], ns[:,2])
    >>> thx = np.rad2deg(thx)
    >>> thy = np.rad2deg(thy)
    
    >>> _ = plt.figure()
    >>> _ = plt.semilogx(rts, thx)
    >>> _ = plt.semilogx(rts, thy)
    
    '''
    
    # set model
    if mode == 0:
        # generate model_class with passed function
        model_class = _model_class_gen(model_f, p0)
    elif mode == 1:
        # linear
        model_class = _Plane3dModel
    elif mode == 2:
        # quadratic
        model_class = _Poly3dModel
    elif mode == 3:
        # quadratic
        model_class = _Poly3dParaboloidModel
    
    # set data
    yy, xx = np.indices(im.shape)
    zz = im
    if mask is None:
        keep = (np.ones_like(im)==1).flatten()
    else:
        keep = (mask==False).flatten()
    data = np.column_stack([xx.flat[keep], yy.flat[keep], zz.flat[keep]])
    
    # randomly select data
    sel = np.random.rand(data.shape[0]) <= fract
    data = data[sel.flatten()]
    
    # scale residual, if chosen
    if scale:
        residual_threshold = residual_threshold * np.std(data[:,2])
    
    # do ransac fit
    model, inliers = ransac(data=data,
                            model_class=model_class,
                            min_samples=min_samples, 
                            residual_threshold=residual_threshold,
                            max_trials=max_trials)
    
    if mask is None and fract==1:
        # get fit directly
        fit = model.model_data.reshape(im.shape)
        inliers = inliers.reshape(im.shape)
    else:
        # get fit from model call
        mc = model_class()
        args = (xx.flatten(), yy.flatten(), zz.flatten())
        fit_full = mc.my_model(model.params, *args)
        fit = fit_full.reshape(im.shape)
        
        inliers_nans = np.empty_like(im).flatten()
        inliers_nans[:] = np.nan
        yi = np.indices(inliers_nans.shape)[0]
        
        sel_fit = yi[keep][sel.flatten()]
        inliers_nans[sel_fit] = inliers
        
        inliers = inliers_nans.reshape(im.shape)
        
    # calculate normal for plane
    if mode == 1:
        # linear
        C = model.params
        n = np.array([-C[0], -C[1], 1])
        n_mag = np.linalg.norm(n, ord=None, axis=0)
        n = n/n_mag
    else:
        # quadratics of function
        n = None
    
    return (fit, inliers, n)

