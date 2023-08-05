from distutils.core import setup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

setup(
    name='denny0515',
    version='1.3.0',
    py_modules=['denny0515'],
    author='DennyHan',
    author_email='denny760515@gmail.com',
    url='http://www.headfirstlabs.com',
    description='A simple printer of nested lists',
    )
