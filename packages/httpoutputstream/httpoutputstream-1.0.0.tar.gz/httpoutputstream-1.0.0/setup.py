from setuptools import setup

setup(
  name = 'httpoutputstream',
  packages = ['httpoutputstream'], # this must be the same as the name above
  version = '1.0.0',
  description = 'httplib stream wrapper for response to use send as an output stream',
  author = 'Salim Malakouti',
  author_email = 'salim.malakouti@gmail.com',
  license = 'MIT',
  url = 'https://github.com/salimm/httpoutpustream', # use the URL to the github repo
  download_url = 'https://github.com/salimm/httpoutpustream/archive/1.0.0.tar.gz', # I'll explain this in a second
  keywords = ['streaming', 'http', 'client'], # arbitrary keywords
  classifiers = ['Programming Language :: Python'],
  install_requires=[],
)
