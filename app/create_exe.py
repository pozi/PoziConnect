from distutils.core import setup
import py2exe

#setup(console=['bb.py'])
setup(windows=[{"script":"bb.py","icon_resources":[(1,"lib\gui\groundtruth.ico")]}])
