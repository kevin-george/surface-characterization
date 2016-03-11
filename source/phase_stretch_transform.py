import numpy
from numpy.fft import fft2, ifft2, fftshift
from scipy.stats import itemfreq

class PhaseStretchTransform:
    def compute(self, image):
        result = pst(image)
        max_num = max(result[0,:])
        for index, line in enumerate(result):
            num = max(result[index,:])
            if num > max_num:
                max_num = num

        computed = ((result/max_num) * 3)

        #Calculating and normalizing the histogram
        x = itemfreq(computed.ravel())
        hist = x[:, 1]/sum(x[:, 1])

        return hist

def cart2pol(x, y):
    return numpy.arctan2(y, x), numpy.hypot(x, y)

def pst(image, lpf=0.21, phase_strength=0.48, warp_strength=12.14, thresh_min=-1, thresh_max=0.0019, morph_flag=False):
    image = image.astype(numpy.float64)

    L = 0.5

    x = numpy.linspace(-L, L, image.shape[1])
    y = numpy.linspace(-L, L, image.shape[0])

    X, Y = numpy.meshgrid(x, y)

    THETA, RHO = cart2pol(X, Y)

    X_step = x[1]-x[0]
    Y_step = y[1]-y[0]

    fx = numpy.linspace(-L/X_step, L/X_step, len(x))
    fy = numpy.linspace(-L/Y_step, L/Y_step, len(y))

    fx_step = fx[1]-fx[0]
    fy_step = fy[1]-fy[0]

    FX, FY = numpy.meshgrid(fx_step, fy_step)

    FTHETA, FRHO = cart2pol(FX, FY)

    # lowpass
    sigma = (lpf ** 2) / numpy.log(2)

    image_f = fft2(image)
    image_f = image_f * fftshift(numpy.exp(-(RHO / numpy.sqrt(sigma))**2))
    image_filtered = numpy.real(ifft2(image_f))

    # PST kernel construction
    rws = RHO*warp_strength
    pst_kernel = rws * numpy.arctan(rws) - 0.5*numpy.log(1+(rws**2))
    pst_kernel /= pst_kernel.max()
    pst_kernel *= phase_strength

    # application of the kernel, and phase calculation
    image_processed = ifft2(fft2(image_filtered) * fftshift(numpy.exp(-1j * pst_kernel)))

    result = numpy.angle(image_processed)

    if not(morph_flag):
        return result
    else:
        binary = numpy.zeros_like(image, dtype=bool)

        binary[result > thresh_max] = 1
        binary[result < thresh_min] = 1
        binary[image < image.max() / 20] = 0

        # the matlab version does post-processing (cleaning) here!

        return binary
