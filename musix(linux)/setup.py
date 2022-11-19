from setuptools import setup, find_packages

setup(
    name='musix',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['python-dotenv','google-api-python-client','pafy','python-vlc','youtube-dl','PyInquirer','pyfiglet','pynput','ewmh','evdev'],
    entry_points='''
    [console_scripts]
    musix=musix:musix
    '''
)