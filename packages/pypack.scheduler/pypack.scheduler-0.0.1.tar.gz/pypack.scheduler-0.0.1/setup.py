from setuptools import setup, find_packages

NAME    = 'scheduler'
VERSION = '0.0.1'
URL     = 'http://github.com/pypack/pypack.scheduler'

setup (
    name    = 'pypack.{}'.format(NAME),
    version = VERSION,
    url     = URL,
    
    description = '',
    long_description = '',
    author='Giovanni Cardamone (MrStep)',
    author_email='g.cardamone2@gmail.com',
    license='MIT',
    classifiers=[
    ],
    keywords='pypack {}'.format(NAME),
    packages= ['pypack/{}'.format(NAME)], #find_packages(exclude=['contrib', 'docs', 'tests*']),
    data_files=[],
    install_requires=[],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            # 'sample=sample:main',
        ],
    },

)
