from distutils.core import setup
import mavapi.api

setup(
    name='mav_api',
    version=mavapi.api.__version__,
    packages=['mavapi'],
    install_requires=['asyncio', 'aiohttp'],
    url='https://github.com/Ar4ikov/mavapi',
    license='Apache 2.0',
    author='Nikita Archikov',
    author_email='bizy18588@gmail.com',
    description='A simple MAV API wrapper for python (3.5 or newer)',
    keywords='mavapi, mav, api, wrappper, rugaming', requires=['aiohttp']

)
