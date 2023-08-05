from distutils.core import setup

setup(
    name='plaitpy',
    version='0.0.9',
    author='okay',
    author_email='okay.zed+pltpy@gmail.com',
    packages=['plaitpy' ],
    package_dir={ 'plaitpy': 'src' },
    scripts=['bin/plait.py'],
    package_data={'plaitpy': [
        '../README.md',
        './*',
        '../templates/*/*',
        '../vendor/faker/lib/locales/*/*.yml',
        '../vendor/faker/lib/locales/*.yml',
    ]},
    url='http://github.com/plaitpy/plaitpy',
    license='MIT',
    description='a fake data generator',
    long_description=open('README.md').read(),
    install_requires=[ ],
    )
