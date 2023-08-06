from setuptools import setup

setup(
  name = 'pylods-json',
  packages = ['pylodsjson'], # this must be the same as the name above
  version = '0.3.1',
  description = 'Pylods, is a python library for object deserialization and serialization. Pylods provides tools to allow automatic recursive serialization of class instances and implementation of customizes rs and deserializers similar to JacksonJson for java. It currently supports JSON and Msgpack',
  author = 'Salim Malakouti',
  author_email = 'salim.malakouti@gmail.com',
  license = 'MIT',
  url = 'https://github.com/salimm/pylods-ijson', # use the URL to the github repo
  download_url = 'http://github.com/salimm/pylods/archive/0.1.0.tar.gz', # I'll explain this in a second
  keywords = ['python','serialization','deserialization','paser','json','object oriented','fast','extendable','type based','jackson json', 'ijson'], # arbitrary keywords
  classifiers = ['Programming Language :: Python'],
  install_requires=['pylods','ijson'],
)
