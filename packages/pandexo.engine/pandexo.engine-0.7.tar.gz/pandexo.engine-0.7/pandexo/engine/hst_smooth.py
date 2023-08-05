import numpy as np

def smooth(x,window_len=10,window='hanning'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    Parameters
    ----------
    x : array of floats
        the input signal 
    window_len : int
        (Optional) Default=10. The dimension of the smoothing window
    window : str
        the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
        flat window will produce a moving average smoothing.
    
    Returns
    -------
    array of floats
        The smoothed signal
        
    Examples
    --------
    >>> t=linspace(-2,2,0.1)
    >>> x=sin(t)+randn(len(t))*0.1
    >>> y=smooth(x)
    
    See Also
    -------- 
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    Todos
    -----
    The window parameter could be the window itself if an array instead of a string
	Source: http://www.scipy.org/Cookbook/SignalSmooth		2009-03-13 
    """

    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")


    #s=numpy.r_[2*x[0]-x[window_len:1:-1],x,2*x[-1]-x[-1:-window_len:-1]]
    s=np.r_[2*np.median(x[0:int(window_len/5)])-x[window_len:1:-1],x,2*np.median(x[-int(window_len/5):])-x[-1:-window_len:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='same')
    return y[window_len-1:-window_len+1]

def medfilt(x, window_len):
    """Apply a length-k median filter to a 1D array x.
    Boundaries are extended by repeating endpoints.
    """
    assert x.ndim == 1, "Input must be one-dimensional."
    if window_len % 2 == 0:
        print(("Median filter length ("+str(window_len)+") must be odd. Adding 1."))
        window_len += 1
    k2 = (window_len - 1) // 2
    s=np.r_[2*np.median(x[0:int(window_len/5)])-x[window_len:1:-1],x,2*np.median(x[-int(window_len/5):])-x[-1:-window_len:-1]]
    y = np.zeros ((len (s), window_len), dtype=s.dtype)
    y[:,k2] = s
    for i in range (k2):
        j = k2 - i
        y[j:,i] = s[:-j]
        y[:j,i] = s[0]
        y[:-j,-(i+1)] = s[j:]
        y[-j:,-(i+1)] = s[-1]
    return np.median(y[window_len-1:-window_len+1], axis=1)