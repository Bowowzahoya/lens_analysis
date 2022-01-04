from setuptools import setup, find_packages

setup(
    name='lens_analysis',
    packages=["lens_analysis"],
    package_dir={"":"src"},
    url='https://github.com/Bowowzahoya/lens_analysis',
    description='Analysis of Lens patent exports',
    long_description=open('README.txt', encoding="utf-8").read(),
    install_requires=[
        "pandas",
        ],
    include_package_data=True,
)