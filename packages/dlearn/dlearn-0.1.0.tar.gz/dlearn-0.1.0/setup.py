from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='dlearn',
      version='0.1.0',
      description='A collection of python modules for machine learning.',
      long_description=readme(),
      classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
      ],
      keywords='machine learning preprocessing cluster',
      url='https://github.com/de-eplearn/dlearn',
      author='Dirk Elsinghorst',
      author_email='de.eplearn5@gmail.com',
      license='MIT',
      packages=['dlearn'],
      install_requires=[
          'numpy',
          'sklearn',
      ],
      zip_safe=False)