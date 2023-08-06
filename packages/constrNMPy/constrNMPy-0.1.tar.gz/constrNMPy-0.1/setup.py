from setuptools import setup

setup(name='constrNMPy',
      version='0.1',
      description='A Python package for constrained Nelder-Mead optimization.',
      url='https://github.com/alexblaessle/constNMPy/',
      author='Alexander Blaessle',
      author_email='alexander.blaessle@gmail.com',
      license='GNU GPL v3',
      packages=['constrNMPy'],
      classifiers=[
	      'Development Status :: 4 - Beta',
	      'Intended Audience :: Science/Research',
	      'Topic :: Scientific/Engineering',
	      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
	      'Programming Language :: Python :: 2.7',
	      'Programming Language :: Python :: 3',
	      'Programming Language :: Python :: 3.2',
	      'Programming Language :: Python :: 3.3',
	      'Programming Language :: Python :: 3.4',
	      ],
      keywords='Optimization Nelder-Mead Constrained',
      install_requires=['numpy','scipy',],
      zip_safe=False)