import os
from setuptools import setup, find_packages
from pip.req import parse_requirements

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_counter_field_py3',
    version='0.0.4',
    packages=find_packages(exclude=['tests']),
    license='MIT License',
    description='python3 fork of django-counter-field',
    long_description=README,
    url='https://github.com/danilke/django_counter_field_py3',
    author='Danila Kulakov, Ian Price',
    author_email='kdanilke@gmail.com, iprice@thermaline.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django-model-changes-py3',
    ],
    test_suite='runtests.runtests',
    tests_require=[
        'pysqlite',
        'django'
    ],
    zip_safe=False,
)
