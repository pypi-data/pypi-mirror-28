import re
from setuptools import setup

version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('pyEfsMounter/__init__.py').read(),
    re.M
    ).group(1)

with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(name='py-efs-mounter',
      description='Mount and unmount to efs',
      entry_points = {
        'console_scripts': ['py-efs-mounter=pyEfsMounter.main:main']
        },
      url='https://github.com/njfix6/py-efs-mounter',
      author='Nicholas Fix',
      author_email='njfix6@gmail.com',
      packages=['pyEfsMounter'],
      long_description = long_descr,
      version=version
)
