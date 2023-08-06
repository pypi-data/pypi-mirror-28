# coding: utf-8

#import sys
#try:
#    reload(sys)
#    sys.setdefaultencoding("utf-8")
#except:
#    print('python3')

from .base import string2second, extract_date, dfcat2n, dfcat2dummy, base_main

__version__ = '0.1'
__license__ = 'MIT'

__all__ = ['string2second', 'extract_date', 'dfcat2n', 'dfcat2dummy']

def main():
    print 'executing...'
    base_main()

