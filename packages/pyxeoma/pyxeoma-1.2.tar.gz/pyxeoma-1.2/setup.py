from setuptools import setup

setup(
    name='pyxeoma',
    packages=['pyxeoma'],
    version='1.2',  # Ideally should be same as your GitHub release tag version
    description='Python wrapper for Xeoma web server API',
    author='Jerad Meisner',
    author_email='jerad.meisner@gmail.com',
    url='https://github.com/jeradM/pyxeoma',
    download_url='https://github.com/jeradM/pyxeoma/archive/1.2.tar.gz',
    keywords=['Xeoma'],
    install_requires=[
        'aiohttp'
    ],
    classifiers=[]
)
