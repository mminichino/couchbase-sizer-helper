from setuptools import setup, find_packages
import cbsizerhelper
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='cbsizerhelper',
    version=cbsizerhelper.__version__,
    packages=find_packages(exclude=['tests']),
    url='https://github.com/mminichino/couchbase-sizer-helper',
    license='MIT License',
    author='Michael Minichino',
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'create_import = cbsizerhelper.create_import:main',
        ]
    },
    install_requires=[
        "attrs>=19.3.0",
    ],
    author_email='info@unix.us.com',
    description='Sizer Helper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=["sizer", "helper"],
    classifiers=[
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: MIT License",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Topic :: Software Development :: Libraries",
          "Topic :: Software Development :: Libraries :: Python Modules"],
)
