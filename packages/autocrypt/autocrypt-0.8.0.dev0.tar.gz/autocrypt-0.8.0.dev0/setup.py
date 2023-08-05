import os
from setuptools import setup

def main():
    with open(os.path.join("autocrypt", "__init__.py")) as f:
        for line in f:
            if "__version__" in line.strip():
                version = line.split("=", 1)[1].strip().strip('"')
                break

    with open("README.rst") as f:
        long_desc = f.read()

    setup(
        name='autocrypt',
        description='(former) autocrypt package',
        long_description = long_desc,
        version='0.8.0.dev0',
        url='https://autocrypt.org',
        license='MIT license',
        platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
        author='holger krekel and the autocrypt team',
        author_email='holger@merlinux.eu',
    )

if __name__ == '__main__':
    main()

