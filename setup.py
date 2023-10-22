from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = f.read()

setup(name='ipythonblocks',
      version='1.9.1',
      description='Practice Python with colored grids in the IPython Notebook',
      long_description=long_description,
      author='Matt Davis',
      author_email='jiffyclub@gmail.com',
      url='https://github.com/jiffyclub/ipythonblocks/',
      packages=find_packages(exclude=['*.test']),
      classifiers=['License :: OSI Approved :: MIT License',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Intended Audience :: Education',
                   'Topic :: Education'],
      install_requires=[
            'ipython>=4.0',
            'notebook>=4.0',
            'requests>=1.0',
      ])
