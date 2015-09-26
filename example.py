# Code Sample for "Processing RAW Images in Python", Pavel Rojtberg, 2015

import libraw              # for loading
import numpy as np         # for processing

proc = libraw.LibRaw()     # create RAW processor
proc.open_file("file.dng") # open file
proc.unpack()              # extract mosaic from file
mosaic = proc.imgdata.rawdata.raw_image

## Listing 1: Mapping to Linear Values
linear = range(2**16)              # a linear LUT
lin_lut = proc.imgdata.color.curve # linearization LUT

if any(lin_lut != linear):
    mosaic = lin_lut[mosaic]       # apply LUT

black = mosaic.min()#proc.imgdata.color.black
saturation = proc.imgdata.color.maximum

uint14_max = 2**14 - 1
mosaic -= black                    # black subtraction
mosaic *= int(uint14_max/(saturation - black))
mosaic = np.clip(mosaic,0,uint14_max)  # clip to range

## Listing 2: White Balancing
assert(proc.imgdata.idata.cdesc == b"RGBG")

cam_mul = proc.imgdata.color.cam_mul # RGB multipliers
cam_mul /= cam_mul[1]                # scale green to 1
mosaic[0::2, 0::2] *= cam_mul[0]     # scale reds
mosaic[1::2, 1::2] *= cam_mul[2]     # scale blues
mosaic = np.clip(mosaic,0,uint14_max)# clip to range

## Listing 3: Demosaicing
def demosaic(m):
    r = m[0::2, 0::2]
    g = np.clip(m[0::2, 1::2]//2 + m[1::2, 0::2]//2,
                0, 2 ** 16 - 1)
    b = m[1::2, 1::2]
    return np.dstack([r, g, b])

mosaic *= 2**2        # expand to 16bit for demosaicing
img = demosaic(mosaic)          # displayable rgb image

## Listing 4: Color Space Conversion
cam2srgb = proc.imgdata.color.rgb_cam[:, 0:3]
cam2srgb = np.round(cam2srgb*255).astype(np.int16)
img = img // 2**8        # reduce dynamic range to 8bpp      
shape = img.shape
pixels = img.reshape(-1, 3).T     # 3xN array of pixels
pixels = cam2srgb.dot(pixels)//255
img = pixels.T.reshape(shape)
img = np.clip(img, 0, 255).astype(np.uint8)

## Listing 5: Gamma Correction
gcurve = [(i / 255) ** (1 / 2.2) * 255 for i in range(256)]
gcurve = np.array(gcurve, dtype=np.uint8)

img = gcurve[img]  # apply gamma LUT

## show info and save output
print("libraw version:", libraw.version())
print("white balance multipliers", cam_mul[:-1])
import matplotlib.image
matplotlib.image.imsave("out.png", img)