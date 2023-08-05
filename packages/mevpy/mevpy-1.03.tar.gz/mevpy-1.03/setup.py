

from distutils.core import setup

setup(
   name='mevpy',
   version='1.03',
   license='MIT',
   description='mevpy package',
   author='Enrico Zorzetto',
   author_email='enrico.zorzetto@duke.edu',
   url = 'https://github.com/EnricoZorzetto/mevpy',
   download_url = 'https://github.com/EnricoZorzetto/mevpy/archive/1.03.tar.gz',
   packages=['mevpy'],  
   install_requires=['matplotlib', 'pandas', 'numpy', 'scipy'], 
   python_requires='>=3',
)


