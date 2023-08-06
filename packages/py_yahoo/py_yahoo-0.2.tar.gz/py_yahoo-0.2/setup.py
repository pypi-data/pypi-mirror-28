from distutils.core import setup
setup(
  name = 'py_yahoo',
  packages = ['py_yahoo'], 
  version = '0.2',
  description = 'A Python Wrapper for Yahoo Weather',
  author = 'Sathesh Rgs',
  author_email = 'satheshrgs@gmail.com',
  url = 'https://github.com/satheshrgs/py_yahoo', 
  download_url = 'https://github.com/satheshrgs/py_yahoo/archive/0.1.tar.gz', 
  keywords = ['yahoo weather', 'wrapper'], 
  license='MIT',
  classifiers = ['Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          "Topic :: Software Development :: Libraries",
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6'],
  install_requires=[
          'requests']
)