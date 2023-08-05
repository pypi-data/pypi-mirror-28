# coding: utf8

__author__ = 'lich666dead'
__title__ = 'BasiliskJS'
__version__ = '0.8'
__copyright__ = 'copyright: (c) 2017 by lich666dead.'


try:
    from .basilisk import PhantomJS
except ImportError:
    from basilisk import PhantomJS
