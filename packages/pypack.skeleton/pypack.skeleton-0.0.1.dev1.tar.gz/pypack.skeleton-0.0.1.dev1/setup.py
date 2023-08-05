from setuptools import setup, find_packages

NAME    = 'pypack.skeleton'
VERSION = '0.0.1.dev1'
URL     = 'http://github.com/pipack/test'

setup (
    name    = NAME,
    version = VERSION,
    url     = URL,
    
    description = '',
    long_description = '',
    author='Giovanni Cardamone (MrStep)',
    author_email='g.cardamone2@gmail.com',
    license='MIT',
    classifiers=[
    ],
    keywords='pipack',
    packages= ['pipack/skeleton'], #find_packages(exclude=['contrib', 'docs', 'tests*']),
    data_files=[],
    install_requires=[],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            # 'sample=sample:main',
        ],
    },

)