from setuptools import setup, find_packages

NAME    = 'skeleton'
VERSION = '0.0.1.dev3'
URL     = 'http://github.com/pipack/{}'.format(NAME)

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
    keywords='pypack',
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