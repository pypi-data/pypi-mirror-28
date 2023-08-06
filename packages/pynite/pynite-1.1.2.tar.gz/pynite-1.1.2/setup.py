from setuptools import setup, find_packages
# SharpBit told me to edit something
setup(
    name='pynite',
    version='1.1.2',
    description='An asynchronous Python API wrapper for the Fortnite API',
    long_description="Asynchronous python wrapper for the Fortnite API.",
    url='https://github.com/cree-py/pynite',
    author='SharpBit and Umbresp',
    author_email='creepy.org3301@gmail.com',
    license='MIT',
    keywords=['fortnite pynite api-wrapper async'],
    packages=find_packages(),
    install_requires=['aiohttp', 'python-box']
)
