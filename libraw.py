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
        ('xtrans', c_char * 6 * 6),
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
        ('curve', c_ushort * 0x10000),
        ('cblack', c_uint * 4),
        ('black', c_uint),
        ('data_maximum', c_uint),
        ('maximum', c_uint),
        ('white', c_ushort * 8 * 8),
        ('cam_mul', c_float * 4),
        ('pre_mul', c_float * 4),
        ('cmatrix', c_float * 3 * 4),
        ('rgb_cam', c_float * 3 * 4),
        ('cam_xyz', c_float * 4 * 3),
        ('phase_one_data', ph1_t),
        ('flash_used', c_float),
        ('canon_ev', c_float),
        ('model2', c_char * 64),
        ('profile', c_void_p),
        ('profile_length', c_uint),
        ('black_stat', c_uint * 8),
    ]


class libraw_imgother_t(Structure):
    _fields_ = [
        ('iso_speed', c_float),
        ('shutter', c_float),
        ('aperture', c_float),
        ('focal_len', c_float),
        ('timestamp', c_uint),  # time_t
        ('shot_order', c_uint),
        ('gpsdata', c_uint * 32),
        ('desc', c_char * 512),
        ('artist', c_char * 64),
    ]


class libraw_thumbnail_t(Structure):
    _fields_ = [
        ('tformat', c_uint),  # LibRaw_thumbnail_formats
        ('twidth', c_ushort),
        ('theight', c_ushort),
        ('tlength', c_uint),
        ('tcolors', c_int),
        ('thumb', POINTER(c_char)),
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
        ('raw_image', POINTER(c_ushort)),
        ('color4_image', POINTER(c_ushort * 4)),
        ('color3_image', POINTER(c_ushort * 3)),
        ('ph1_black', POINTER(c_short * 2)),
        ('iparams', libraw_iparams_t),
        ('sizes', libraw_image_sizes_t),
        ('ioparams', libraw_internal_output_params_t),
        ('color', libraw_colordata_t),
    ]


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
        ('output_profile', POINTER(c_char)),
        ('camera_profile', POINTER(c_char)),
        ('bad_pixels', POINTER(c_char)),
        ('dark_frame', POINTER(c_char)),
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
        ('no_auto_scale', c_int),
        ('no_interpolation', c_int),
        ('straw_ycc', c_int),
        ('force_foveon_x3f', c_int),
    ]


class libraw_data_t(Structure):
    _fields_ = [
        ('image', POINTER(c_ushort * 4)),
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
    
_hdl.libraw_init.restype = POINTER(libraw_data_t)
_hdl.libraw_unpack_function_name.restype = c_char_p
_hdl.libraw_strerror.restype = c_char_p
_hdl.libraw_version.restype = c_char_p

_from_memory = ctypes.pythonapi.PyMemoryView_FromMemory if sys.version_info.major >= 3 else pythonapi.PyBuffer_FromMemory
_from_memory.restype = ctypes.py_object

def strerror(e):
    return _hdl.libraw_strerror(e).decode("utf-8")

def version():
    return _hdl.libraw_version().decode("utf-8")

class LibRaw:
    def __init__(self, flags = 0):
        self._proc = _hdl.libraw_init(flags)
            
    def __getattr__(self, name):
        try:
            # try handling as an attrribute
            val = getattr(self._proc.contents, name)
            setattr(self, name, val)  # cache value
            return val
        except AttributeError:
            pass
        
        # then this must be a method
        rawfun = getattr(_hdl, "libraw_" + name)
        
        def handler(*args):
            return rawfun(self._proc, *args)
        
        setattr(self, name, handler)  # cache value
        return handler
    
    @property
    def image(self):
        """
        @return: image as numpy array
        """
        S = self.sizes
        size = S.iwidth * S.iheight * 4 * 2  # 4 channel, 2 byte per pixel
        buffer = _from_memory(self._proc.contents.image, size)
        arr = np.frombuffer(buffer, np.uint16)
        return arr.reshape(S.iheight, S.iwidth, 4)
    
    def open_file(self, filename):
        e = _hdl.libraw_open_file(self._proc, filename.encode('utf-8'))
        if e != 0:
            raise Exception(strerror(e))
    
    def dcraw_ppm_tiff_writer(self, filename):
        e = _hdl.libraw_dcraw_ppm_tiff_writer(self._proc, filename.encode('utf-8'))
        if e != 0:
            raise Exception(strerror(e))
        
if __name__ == "__main__":    
    if len(sys.argv) < 3:
        print("usage {} <rawfile> <outfile>.ppm".format(sys.argv[0]))
        sys.exit(1)
    
    proc = LibRaw()
    # Load the RAW file 
    proc.open_file(sys.argv[1])   
    
    # Develop the RAW file
    proc.unpack()
    proc.dcraw_process()
    proc.dcraw_ppm_tiff_writer(sys.argv[2])
