from setuptools import setup

setup(  
    name="tj",
    version=raw_input('Enter version:'),
    description="A very simple short module containing useful functions",
    long_description="A module that have powerful and simple functions. Read README.txt for more info",
    author="Tushar Jain",
    author_email="tusharlock10@gmail.com",
    py_modules=['tj'],
    install_requires=['Crypto']
)
