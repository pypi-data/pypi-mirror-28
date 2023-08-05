from setuptools import setup, find_packages

setup(
    name = 'cnfaker',
    version = '0.1.7',
    keywords='faker generate chinese words',
    description = 'a library for chinese words or other things filling ',
    license = 'MIT License',
    url = 'https://github.com/hjlarry/cnfaker',
    author = 'hjlarry',
    author_email = 'hjlarry@163.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
)