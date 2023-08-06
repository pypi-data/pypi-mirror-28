from setuptools import find_packages, setup


with open('README.rst') as fd:
    long_description = fd.read()

with open('requirements/common.txt') as f:
    requirements = f.read().splitlines()

with open('requirements/tests.txt') as f:
    test_requirements = f.read().splitlines()

with open('requirements/docs.txt') as f:
    docs_requirements = f.read().splitlines()


setup(
    name='objectipy',
    version='0.0.1a1',
    author='Sergey Tsaplin',
    author_email='me@sergeytsaplin.com',
    description='Any to python objects deserializer with value validations',
    long_description=long_description,
    license='MIT',
    packages=find_packages(exclude=['tests', 'examples']),
    install_requires=requirements,
    extras_require={
        'test': test_requirements,
        'docs': docs_requirements,
    },
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
)
