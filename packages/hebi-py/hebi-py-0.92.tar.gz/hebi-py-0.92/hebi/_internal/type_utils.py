# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  HEBI Core python API - Copyright 2018 HEBI Robotics
#  See http://hebi.us/softwarelicense for license details
#
# -----------------------------------------------------------------------------
"""
Internally used procedures to convert from and to types. Functions here aren't
part of the public API and may change without notice.
"""

from ctypes import Array, create_string_buffer
from numpy import float64, asmatrix, ascontiguousarray, matrix
from sys import version_info

def to_mac_address(*args):
  """
  Convert input argument(s) to a MacAddress object.
  Only 1 or 6 arguments are valid.

  If 1 argument is provided, try the following:

    * If input type is MacAddress, simply return that object
    * If input type is list or ctypes Array, recall with these elements
    * If input is of another type, try to parse a MAC address from its
      `__str__` representation

  When 6 parameters are provided, this attempts to construct a MAC address
  by interpreting the input parameters as sequential bytes of a mac address.

  If the provided argument count is neither 1 or 6,
  this function throws an exception.

  :param args: 1 or 6 element list of variadic arguments
  :return: a MacAddress instance
  """
  from .lookup import MacAddress, _mac_address_from_string, _mac_address_from_bytes

  if (len(args) == 1):
    if (type(args[0]) == MacAddress):
      return args[0]
    elif(isinstance(args[0], list) or isinstance(args[0], Array)):
      if (len(args[0]) == 1):
        return to_mac_address(args[0])
      elif(len(args[0]) == 6):
        arg = args[0]
        return to_mac_address(arg[0], arg[1], arg[2], arg[3], arg[4], arg[5])
      else:
        raise ValueError('Invalid amount of arguments provided')
    else:
      try:
        return _mac_address_from_string(args[0])
      except ValueError as v:
        raise RuntimeError(
          'Could not create mac address from argument', v)

  elif (len(args) == 6):
    return _mac_address_from_bytes(args[0], args[1], args[2],
                                   args[3], args[4], args[5])
  else:
    raise RuntimeError('Invalid amount of arguments provided')


def is_matrix_or_matrix_convertible(val):
  """
  XXX Document!

  :param val:
  :return:
  """
  if (isinstance(val, matrix)):
    shape = val.shape
    if (shape[0] == 1 or shape[1] == 1):
      return False
    return True
  try:
    m = asmatrix(val)
    if (m.shape[0] == 1 or m.shape[1] == 1):
      return False
    return True
  except:
    return False


# -----------------------------------------------------------------------------
# Converting to numpy types
# -----------------------------------------------------------------------------


def to_contig_sq_mat(mat, dtype=float64, size=3):
  """
  Converts input to a numpy square matrix of the specified data type and size.

  This function ensures that the underlying data is laid out
  in contiguous memory.

  :param mat: Input matrix
  :param dtype: Data type of matrix
  :param size: Size of matrix
  :return: a `size`x`size` numpy matrix with elements of type `dtype`
  """
  ret = asmatrix(mat, dtype=dtype)

  # Is array-like
  if (ret.shape[0] == 1):
    # Will fail if not len of `size`*`size`
    ret = ret.reshape(size, size)

  # Enforce output will be right shape
  if (ret.shape != (size, size)):
    raise ValueError('Cannot convert input to shape {0}'.format((size, size)))

  # Enforce contiguous in memory
  if not ret.flags['C_CONTIGUOUS']:
    ret = ascontiguousarray(ret)

  return ret


# -----------------------------------------------------------------------------
# CTypes Compatibility functions
# -----------------------------------------------------------------------------


def create_string_buffer_compat(init, size=None):
  """
  Enables compatibility between Python 2 and 3

  :param init:
  :param size:
  :return:
  """
  if (version_info[0] == 2):
    return create_string_buffer(init, size)
  elif (size == None):
    return create_string_buffer(init)
  else:
    return create_string_buffer(bytes(init, 'utf8'), size)


def decode_string_buffer(bfr, encoding='utf8'):
  if (type(bfr) == str):
    return bfr
  elif (version_info[0] == 3):
    return bfr.decode(encoding)


def create_double_buffer(size):
  from ctypes import c_double
  return (c_double * size)()