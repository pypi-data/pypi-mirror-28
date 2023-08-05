from setuptools import setup


setup(
    name='soundcloud-lib',
    version='0.2.2',
    description='Python Soundcloud API',
    long_description='',
    url='https://github.com/3jackdaws/soundcloud-lib',
    author='Ian Murphy',
    author_email='3jackdaws@gmail.com',
    license='MIT',
    packages=['sclib'],
    install_requires=['mutagen', 'bs4'],
    test_suite='pytest',
    tests_require=['pytest'],
)