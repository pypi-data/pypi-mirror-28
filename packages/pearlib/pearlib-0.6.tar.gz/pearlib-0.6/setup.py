from setuptools import setup

def readme():
	with open('README.rst') as f:
		return f.read()

setup(name = 'pearlib',
      version = '0.6',
      description = 'The library that makes neural networks appear',
      long_description = readme(),
      classifiers = [
      'Development Status :: 3 - Alpha',
      'License :: OSI Approved :: BSD License',
      'Natural Language :: English',
      'Programming Language :: Python :: 3.6',
      'Topic :: Scientific/Engineering :: Visualization',
      'Framework :: IDLE'],
      keywords = 'tensorflow neural networks visualization',
      python_requires = '>=3',
      url = 'https://github.com/danimano/TRP',
      author = 'Candice Bentéjac, Anna Csorgo, Daniel Hajto',
      author_email = 'candice.bentejac@etu.u-bordeaux.fr',
      license = 'BSD-3-Clause',
      packages = ['pearlib'],
      install_requires = ['numpy', 'matplotlib', 'pillow', 'tensorflow', 'webcolors'],
      zip_safe = False)

