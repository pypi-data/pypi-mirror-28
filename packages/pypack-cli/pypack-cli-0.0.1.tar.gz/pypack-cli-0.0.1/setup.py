from setuptools import setup, find_packages

NAME    = 'pypack-cli'
VERSION = '0.0.1'
URL     = 'http://github.com/pypack/{}'.format(NAME)

setup (
    name    = NAME,
    version = VERSION,
    url     = URL,
    
    description = 'pypack cli interface',
    long_description = '',
    author='Giovanni Cardamone (MrStep)',
    author_email='g.cardamone2@gmail.com',
    license='MIT',
    classifiers=[
    ],
    keywords='pypack',
    packages= ['pypack/pypack_cli'], #find_packages(exclude=['contrib', 'docs', 'tests*']),
    data_files=[],
    install_requires=[],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'pypack = pypack.pypack_cli:main',
        ],
    },

)
