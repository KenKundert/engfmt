try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='engfmt',
    version='1.0.2',
    description='read and write in engineering notation',
    long_description=readme,
    author="Ken Kundert",
    author_email='engfmt@nurdletech.com',
    url='http://nurdletech.com/linux-utilities/engfmt',
    download_url='https://github.com/kenkundert/engfmt/tarball/master',
    license='GPLv3+',
    zip_safe=True,
    py_modules=['engfmt'],
    install_requires=['six', 'pytest-runner'],
    tests_require=['pytest'],
    keywords=[
        'quantities', 'engfmt', 'engineering', 'notation', 'SI', 'scale factors'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering',
    ],
)
