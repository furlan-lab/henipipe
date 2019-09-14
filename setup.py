import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

    setuptools.setup(
    name="henipipe",
    version="0.2.3",
    author="Scott Furlan",
    author_email="scottfurlan@gmail.com",
    description="A python wrapper for fast processing of sequencing data using CutnRun or CutnTag",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scfurl/henipipe.git",
    packages=setuptools.find_packages(),
    package_data={'henipipe': ['henipipe/data/genomes.json']},
    install_requires=['six >= 1'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.5',
    entry_points={'console_scripts': [
        'henipipe = henipipe.__main__:run_henipipe',
        'samTobed = henipipe.samTobed:run_sam2bed',
        'pyWriter = henipipe.pyWriter:run_pyWriter',
    ]},
    )

##Install pipx

#TEST
## run this to make package: python3 setup.py sdist bdist_wheel
## run this to upload to test pypi: twine upload --repository-url https://test.pypi.org/legacy/ dist/*


#TEST INSTALL
# pip install --index-url https://test.pypi.org/henipipe/ henipipe


#FOR REAL
## run this to make package: python3 setup.py sdist bdist_wheel
## run this to upload to pypi: python3 -m twine upload dist/*



##PIPX on PBS
## module load python/3.6.5
## python3 -m pip install --user pipx
## python3 -m pipx ensurepath
## pip install henipipe --trusted-host pypi.org --trusted-host files.pythonhosted.org --user
## pipx uninstall henipipe
## pipx install --spec git+https://github.com/scfurl/henipipe --include-deps henipipe --pip-args '--trusted-host pypi.org --trusted-host files.pythonhosted.org'
## pipx install --include-deps --pip-args '--trusted-host pypi.org --trusted-host files.pythonhosted.org' henipipe
## pipx install --include-deps henipipe

## pipx install --spec git+https://github.com/scfurl/henipipe --include-deps henipipe 

##