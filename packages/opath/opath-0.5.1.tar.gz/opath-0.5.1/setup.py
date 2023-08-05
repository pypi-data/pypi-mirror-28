import os
import re
from distutils.core import setup

tests_require = [
    'pytest',
    'pytest-runner',
    'python-coveralls',
    'pytest-pep8'
]

install_requires = [
    'pathlib'
]


def sanitize_string(str):
    str = str.replace('\"', '')
    str = str.replace("\'", '')
    return str


def parse_version_file():
    """Parse the __version__.py file"""
    here = os.path.abspath(os.path.dirname(__file__))
    ver_dict = {}
    with open(os.path.join(here, 'opath', '__version__.py'), 'r') as f:
        for line in f.readlines():
            m = re.match('__(\w+)__\s*=\s*(.+)', line)
            if m:
                ver_dict[m.group(1)] = sanitize_string(m.group(2))
    return ver_dict


def read(fname):
    """Read a file"""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


ver = parse_version_file()

# setup
setup(
        name=ver['title'],
        version=ver['version'],
        packages=[ver['package']],
        url='https://github.com/jvrana/opath',
        license=ver['license'],
        author=ver['author'],
        author_email='justin.vrana@gmail.com',
        keywords='directory python tree path',
        description='intuitive python directory tree management for all',
        long_description=read("README"),
        install_requires=install_requires,
        python_requires='>=3.3',
        tests_require=tests_require,
)
