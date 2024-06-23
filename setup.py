# setup.py

from setuptools import setup, find_packages

setup(
    name="Flask-DebugToolbar-DjangoSQL",
    version="0.1.2",
    description="A Flask Debug Toolbar panel for Django SQL queries.",
    author="Joey",
    author_email="qiuyu.an@hotmail.com",
    url="https://github.com/anqiuy/flask_debugtoolbar_djangosql",
    license="MIT",
    packages=find_packages(exclude=('example', )),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-DebugToolbar',
        'Django',
        # Add any other dependencies here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
