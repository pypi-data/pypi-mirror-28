from setuptools import setup, find_packages

setup(
    name = 'shw',
    version = '0.2.0',
    keywords='ssh shortcut ubuntu',
    description = 'a library for ssh & scp shortcut on linux',
    license = 'MIT License',
    url = '',
    author = 'wong',
    author_email = 'yachenwang4@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
    scripts = [],
    entry_points = {
        'console_scripts': [
            'shw = shw.main:main'
        ] 
    }
)
