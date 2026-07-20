from setuptools import setup, find_packages

setup(
    name="LM3-vasp-tools",
    version="0.1.0",
    description="A Python library for VASP analysis in LM3 Lab",
    author="Won June Kim",
    license="LM3 Lab",

    packages=find_packages(),
    python_requires=">=3.7",

    include_package_data=True,

    zip_safe=False,
)
