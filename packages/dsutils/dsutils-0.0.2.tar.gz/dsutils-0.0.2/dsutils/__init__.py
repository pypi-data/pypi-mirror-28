# coding: utf-8

#import sys
#try:
#    reload(sys)
#    sys.setdefaultencoding("utf-8")
#except:
#    print('python3')

from .base import PipelineLDA
from .base import main as LDA_main



def main():
    print 'executing...'
    LDA_main()

