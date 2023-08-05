from setuptools import setup, find_packages
pkg = "staticsubset"
ver = '0.0.1'
setup(name             = pkg,
      version          = ver,
      description      = "static subset",
      long_description =
      "Generate symlinks for every file and directory in a tree",
      author           = "Eduard Christian Dumitrescu",
      license          = "LGPLv3",
      url              = "https://hydra.ecd.space/f/staticsubset/",
      packages         = find_packages(),
      install_requires = [],
      entry_points     = {
          'console_scripts': ['staticsubset='+pkg+'.main:main']},
      classifiers      = ["Programming Language :: Python :: 3 :: Only"])
