from setuptools import setup

setup(
  name = 'lessrpc_common',
  packages = ['lessrpc_common'], # this must be the same as the name above
  version = '1.0.4',
  description = 'Less RPC Common modules share between stubs, name server and extensions',
  author = 'Salim Malakouti',
  author_email = 'salim.malakouti@gmail.com',
  license = 'MIT',
  url = 'https://github.com/LessRPC/lessrpc_common', # use the URL to the github repo
  download_url = 'https://github.com/LessRPC/lessrpc_common/archive/1.0.2.tar.gz', # I'll explain this in a second
  keywords = ['python','serialization','deserialization','rpc','rmi','less rpc'], # arbitrary keywords
  classifiers = ['Programming Language :: Python :: 2.7'],
  install_requires=[]
)
