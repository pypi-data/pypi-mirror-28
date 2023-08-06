from setuptools import setup

setup(name='sqlplus',
      version='1.0.9',
      description='data work tools',
      url='https://github.com/nalssee/sqlplus.git',
      author='nalssee',
      author_email='kenjin@sdf.org',
      license='MIT',
      packages=['sqlplus'],
      # Install statsmodels manually with conda install
      install_requires=[
          'sas7bdat==2.0.7',
          'xlrd==1.1.0'
      ],
      scripts=['bin/prepend', 'bin/fnguide'],
      zip_safe=False)
