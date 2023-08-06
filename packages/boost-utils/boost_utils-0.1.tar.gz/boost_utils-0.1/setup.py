from setuptools import setup

setup(name='boost_utils',
      version='0.1',
      description='Boost Real Estate AI utility package',
      long_description='Group of utilities and mostly used, helper utility functions.',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities'
      ],
      keywords='Boost NextAce Fidelity National Real Estate',
      url='http://boost.nextace.com',
      author='Erguder, Freire, Hansen, Zhang',
      author_email='dreez@nextace.com',
      license='MIT',
      packages=['boost_utils'],
      include_package_data=True,
      zip_safe=False)