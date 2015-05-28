#!/usr/bin/python3
"""
@package libraw.py
Python Bindings for libraw

use the documentation of libraw C API for function calls
based on: https://gist.github.com/campaul/ee30b2dbc2c11a699bde

@author: Pavel Rojtberg (http://www.rojtberg.net)
@see: https://github.com/paroj/libraw.py
@copyright: LGPLv2 (same as libraw) <http://opensource.org/licenses/LGPL-2.1>
"""

from ctypes import *
import ctypes.util

import sys
import numpy as np

_hdl = cdll.LoadLibrary(ctypes.util.find_library("raw"))

enum_LibRaw_thumbnail_formats = c_int
time_t = c_long

class ph1_t(Structure):
    _fields_ = [
        ('format', c_int),
        ('key_off', c_int),
        ('t_black', c_int),
        ('black_off', c_int),
        ('split_col', c_int),
        ('tag_21a', c_int),
        ('tag_210', c_float),
    ]


class libraw_iparams_t(Structure):
    _fields_ = [
        ('make', c_char * 64),
        ('model', c_char * 64),
        ('raw_count', c_uint),
        ('dng_version', c_uint),
        ('is_foveon', c_uint),
        ('colors', c_int),
        ('filters', c_uint),
        # ('xtrans', c_char * 6 * 6), # 0.16+
        ('cdesc', c_char * 5),
    ]


class libraw_image_sizes_t(Structure):
    _fields_ = [
        ('raw_height', c_ushort),
        ('raw_width', c_ushort),
        ('height', c_ushort),
        ('width', c_ushort),
        ('top_margin', c_ushort),
        ('left_margin', c_ushort),
        ('iheight', c_ushort),
        ('iwidth', c_ushort),
        ('raw_pitch', c_uint),
        ('pixel_aspect', c_double),
        ('flip', c_int),
        ('mask', c_int * 8 * 4),
    ]


class libraw_colordata_t(Structure):
    _fields_ = [
        ('_curve', c_ushort * 0x10000),
        ('_cblack', c_uint * 4),
        ('black', c_uint),
        ('data_maximum', c_uint),
        ('maximum', c_uint),
        ('white', c_ushort * 8 * 8),
        ('_cam_mul', c_float * 4),
        ('_pre_mul', c_float * 4),
        ('_cmatrix', c_float * 3 * 4),
        ('_rgb_cam', c_float * 3 * 4),
        ('_cam_xyz', c_float * 3 * 4),
        ('phase_one_data', ph1_t),
        ('flash_used', c_float),
        ('canon_ev', c_float),
        ('model2', c_char * 64),
        ('profile', c_void_p),
        ('profile_length', c_uint),
        # ('black_stat', c_uint * 8), # 0.16+
    ]

    @property
    def curve(self):
        return _array_from_memory(self._curve, (0x10000,), np.uint16)

    @property
    def cmatrix(self):
        return _array_from_memory(self._cmatrix, (3, 4), np.float32)

    @property
    def rgb_cam(self):
        return _array_from_memory(self._rgb_cam, (3, 4), np.float32)
    
    @property
    def cam_xyz(self):
        return _array_from_memory(self._cam_xyz, (3, 4), np.float32)
    
    @property
    def cam_mul(self):
        return _array_from_memory(self._cam_mul, (4,), np.float32)

    @property
    def pre_mul(self):
        return _array_from_memory(self._pre_mul, (4,), np.float32)

    @property
    def cblack(self):
        return _array_from_memory(self._cblack, (4,), np.uint)

class libraw_imgother_t(Structure):
    _fields_ = [
        ('iso_speed', c_float),
        ('shutter', c_float),
        ('aperture', c_float),
        ('focal_len', c_float),
        ('timestamp', time_t),
        ('shot_order', c_uint),
        ('gpsdata', c_uint * 32),
        ('desc', c_char * 512),
        ('artist', c_char * 64),
    ]


class libraw_thumbnail_t(Structure):
    _fields_ = [
        ('tformat', enum_LibRaw_thumbnail_formats),
        ('twidth', c_ushort),
        ('theight', c_ushort),
        ('tlength', c_uint),
        ('tcolors', c_int),
        ('thumb', c_char_p),
    ]


class libraw_internal_output_params_t(Structure):
    _fields_ = [
        ('mix_green', c_uint),
        ('raw_color', c_uint),
        ('zero_is_bad', c_uint),
        ('shrink', c_ushort),
        ('fuji_width', c_ushort),
    ]


class libraw_rawdata_t(Structure):
    _fields_ = [
        ('raw_alloc', c_void_p),
        ('_raw_image', POINTER(c_ushort)),
        ('color4_image', POINTER(c_ushort * 4)),
        ('color3_image', POINTER(c_ushort * 3)),
        ('ph1_black', POINTER(c_short * 2)),
        ('iparams', libraw_iparams_t),
        ('sizes', libraw_image_sizes_t),
        ('ioparams', libraw_internal_output_params_t),
        ('color', libraw_colordata_t),
    ]

    @property
    def raw_image(self):
        S = self.sizes
        return _array_from_memory(self._raw_image, (S.raw_height, S.raw_width), np.uint16)

class libraw_output_params_t(Structure):
    _fields_ = [
        ('greybox', c_uint * 4),
        ('cropbox', c_uint * 4),
        ('aber', c_double * 4),
        ('gamm', c_double * 6),
        ('user_mul', c_float * 4),
        ('shot_select', c_uint),
        ('bright', c_float),
        ('threshold', c_float),
        ('half_size', c_int),
        ('four_color_rgb', c_int),
        ('highlight', c_int),
        ('use_auto_wb', c_int),
        ('use_camera_wb', c_int),
        ('use_camera_matrix', c_int),
        ('output_color', c_int),
        ('output_profile', c_char_p),
        ('camera_profile', c_char_p),
        ('bad_pixels', c_char_p),
        ('dark_frame', c_char_p),
        ('output_bps', c_int),
        ('output_tiff', c_int),
        ('user_flip', c_int),
        ('user_qual', c_int),
        ('user_black', c_int),
        ('user_cblack', c_int * 4),
        ('sony_arw2_hack', c_int),
        ('user_sat', c_int),
        ('med_passes', c_int),
        ('auto_bright_thr', c_float),
        ('adjust_maximum_thr', c_float),
        ('no_auto_bright', c_int),
        ('use_fuji_rotate', c_int),
        ('green_matching', c_int),
        ('dcb_iterations', c_int),
        ('dcb_enhance_fl', c_int),
        ('fbdd_noiserd', c_int),
        ('eeci_refine', c_int),
        ('es_med_passes', c_int),
        ('ca_correc', c_int),
        ('cared', c_float),
        ('cablue', c_float),
        ('cfaline', c_int),
        ('linenoise', c_float),
        ('cfa_clean', c_int),
        ('lclean', c_float),
        ('cclean', c_float),
        ('cfa_green', c_int),
        ('green_thresh', c_float),
        ('exp_correc', c_int),
        ('exp_shift', c_float),
        ('exp_preser', c_float),
        ('wf_debanding', c_int),
        ('wf_deband_treshold', c_float * 4),
        ('use_rawspeed', c_int),
        # 0.16+
        # ('no_auto_scale', c_int),
        # ('no_interpolation', c_int),
        # ('straw_ycc', c_int),
        # ('force_foveon_x3f', c_int),
    ]


class libraw_data_t(Structure):
    _fields_ = [
        ('_image', POINTER(c_ushort * 4)),
        ('sizes', libraw_image_sizes_t),
        ('idata', libraw_iparams_t),
        ('params', libraw_output_params_t),
        ('progress_flags', c_uint),
        ('process_warnings', c_uint),
        ('color', libraw_colordata_t),
        ('other', libraw_imgother_t),
        ('thumbnail', libraw_thumbnail_t),
        ('rawdata', libraw_rawdata_t),
        ('parent_class', c_void_p),
    ]

    @property
    def image(self):
        S = self.sizes
        return _array_from_memory(self._image, (S.iheight, S.iwidth, 4), np.uint16)

_hdl.libraw_init.restype = POINTER(libraw_data_t)
_hdl.libraw_unpack_function_name.restype = c_char_p
_hdl.libraw_strerror.restype = c_char_p
_hdl.libraw_version.restype = c_char_p

# buffer from memory definition
_buffer_from_memory = None
if sys.version_info.major >= 3:
    _buffer_from_memory = lambda ptr, size: pythonapi.PyMemoryView_FromMemory(ptr, size, 0x200)  # writable
    pythonapi.PyMemoryView_FromMemory.restype = py_object
else:
    _buffer_from_memory = pythonapi.PyBuffer_FromReadWriteMemory
    _buffer_from_memory.restype = py_object

def _array_from_memory(ptr, shape, type):
    size = int(np.prod(shape) * np.dtype(type).itemsize)
    return np.frombuffer(_buffer_from_memory(ptr, size), type).reshape(shape)
    
def strerror(e):
    return _hdl.libraw_strerror(e).decode("utf-8")

def version():
    return _hdl.libraw_version().decode("utf-8")

def versionNumber():
    v = _hdl.libraw_versionNumber()
    return ((v >> 16) & 0x0000ff, (v >> 8) & 0x0000ff, v & 0x0000ff)
    
class LibRaw:
    def __init__(self, flags=0):
        if versionNumber()[1] > 15:
            sys.stdout.write("libraw.py: warning - structure definitions are not compatible with your version.\n")
        
        self._proc = _hdl.libraw_init(flags)
        assert(self._proc.contents)
        self.imgdata = self._proc.contents
        
    def __getattr__(self, name):
        rawfun = getattr(_hdl, "libraw_" + name)
        
        def handler(*args):
            # do not pass python strings to C
            args = [a.encode("utf-8") if isinstance(a, str) else a for a in args]
            
            e = rawfun(self._proc, *args)
            if e != 0:
                raise Exception(strerror(e))
        
        setattr(self, name, handler)  # cache value
        return handler
        
if __name__ == "__main__":    
    if len(sys.argv) < 3:
        print("usage {} <rawfile> <outfile>".format(sys.argv[0]))
        sys.exit(1)
    
    proc = LibRaw()
    # Load the RAW file 
    proc.open_file(sys.argv[1])   
    
    # Develop the RAW file
    proc.unpack()
    proc.dcraw_process()
    proc.params.output_tiff = sys.argv[2].endswith(".tiff")
    proc.dcraw_ppm_tiff_writer(sys.argv[2])
