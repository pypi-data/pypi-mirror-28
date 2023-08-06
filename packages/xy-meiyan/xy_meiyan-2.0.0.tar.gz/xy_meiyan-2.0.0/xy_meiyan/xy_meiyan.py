from struct import unpack
from scipy import interpolate

from PIL import Image
import numpy
import scipy

import sys
import os

class Filter:

  def __init__(self, acv_file_path, name):
    self.name = name
    with open(acv_file_path, 'rb') as acv_file:
      self.curves = self._read_curves(acv_file)
    self.polynomials = self._find_coefficients()

  def _read_curves(self, acv_file):
    _, nr_curves = unpack('!hh', acv_file.read(4))
    curves = []
    for i in range(0, nr_curves):
      curve = []
      num_curve_points, = unpack('!h', acv_file.read(2))
      for j in range(0, num_curve_points):
        y, x = unpack('!hh', acv_file.read(4))
        curve.append((x,y))
      curves.append(curve)

    return curves

  def _find_coefficients(self):
    polynomials = []
    for curve in self.curves:
      xdata = [x[0] for x in curve]
      ydata = [x[1] for x in curve]
      p = interpolate.lagrange(xdata, ydata)
      polynomials.append(p)
    return polynomials

  def get_r(self):
    return self.polynomials[1]

  def get_g(self):
    return self.polynomials[2]

  def get_b(self):
    return self.polynomials[3]

  def get_c(self):
    return self.polynomials[0]

class FilterManager:

  def __init__(self):
    self.filters = {}
    #add some stuff here

  def add_filter(self,filter_obj):
    # Overwrites if such a filter already exists
    # NOTE: Fix or not to fix?
    self.filters[filter_obj.name] = filter_obj

  def apply_filter(self,filter_name,image_array):

    if image_array.ndim < 3:
      raise Exception('Photos must be in color, meaning at least 3 channels')
    else:
      def interpolate(i_arr, f_arr, p, p_c):
        p_arr = p_c(f_arr)
        return p_arr

      # NOTE: Assumes that image_array is a numpy array
      image_filter = self.filters[filter_name]
      # NOTE: What happens if filter does not exist?
      width,height,channels = image_array.shape
      filter_array = numpy.zeros((width, height, 3), dtype=float)

      p_r = image_filter.get_r()
      p_g = image_filter.get_g()
      p_b = image_filter.get_b()
      p_c = image_filter.get_c()

      filter_array[:,:,0] = p_r(image_array[:,:,0])
      filter_array[:,:,1] = p_g(image_array[:,:,1])
      filter_array[:,:,2] = p_b(image_array[:,:,2])
      filter_array = filter_array.clip(0,255)
      filter_array = p_c(filter_array)

      filter_array = numpy.ceil(filter_array).clip(0,255)

      return filter_array.astype(numpy.uint8)

def meiyan(filename='', style=1):
    ''' 对图片做美颜效果'''
    '''美颜风格'''
    IMG_STYLE = {
        1:'country',
        2:'crossprocess',
        3:'desert',
        4:'lumo',
        5:'nashville',
        6:'portraesque',
        7:'proviaesque',
        8:'velviaesque',
        9:'FA_Curves1',
        10:'FA_Curves2',
        11:'FA_Curves3'
    }
    if filename == '':
        return -1
    res = os.path.abspath(__file__)
    res = os.path.split(res)[0]
    curvefile = res + '/data/' + IMG_STYLE[style] + '.acv'
    img_filter = Filter(curvefile,'crgb')
    im = Image.open(filename)
    image_array = numpy.array(im)
    filter_manager = FilterManager()
    filter_manager.add_filter(img_filter)
    filter_array = filter_manager.apply_filter('crgb', image_array)
    im = Image.fromarray(filter_array)
    new_name = 'meiyan_' + filename
    im.save(new_name)
    im.show()
    return new_name

def main():
    res = meiyan('king1.jpg')
    print(res)
    res = meiyan('king1.jpg',2)
    print(res)
    res = meiyan('king1.jpg',3)
    print(res)
    res = meiyan('king1.jpg',4)
    print(res)
    res = meiyan('king1.jpg',5)
    print(res)
    res = meiyan('king1.jpg',6)
    print(res)
    res = meiyan('king1.jpg',7)
    print(res)
    res = meiyan('king1.jpg',8)
    print(res)
if __name__ == '__main__':
    main()
