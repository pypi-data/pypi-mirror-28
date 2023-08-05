import os
import setuptools


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()


setuptools.setup(
    name='kek',
    version='0.1.0a1',
    description='Simple tool for automating repetitive tasks',
    long_description=long_description,
    url='https://github.com/martyanov/kek',
    author='Andrey Martyanov',
    author_email='andrey@martyanov.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='development',
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests']),
    extras_require={
        'dev': ['twine'],
    },
    python_requires='>=3.4',
    entry_points={
        'console_scripts': [
            'kek=kek.__main__:main',
        ],
    },
)
