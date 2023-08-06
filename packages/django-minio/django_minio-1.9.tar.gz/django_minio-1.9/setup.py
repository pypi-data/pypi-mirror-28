from setuptools import setup, find_packages
import os


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_minio',
    version='1.9',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Django app to use Minio Server as file storage.',
    long_description=README,
    url='https://github.com/shapoglyk/django_minio',
    author='Belek Abylov',
    author_email='abylov.belek@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='minio storage files',
    install_requires=[
        'Django >= 1.7, <1.9',
        'minio == 2.2.2',
    ],
    extras_require={
        'dev': [
            'wheel',
            'twine'
        ],
    },
)
