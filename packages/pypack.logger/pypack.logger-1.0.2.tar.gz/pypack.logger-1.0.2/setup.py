from setuptools import setup, find_packages

NAME    = 'logger'
VERSION = '1.0.2'
URL     = 'http://github.com/pypack/{}'.format(NAME)

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
    keywords='pypack logger',
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