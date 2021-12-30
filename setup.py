from setuptools import setup, find_packages

setup(
    name='lens_analysis',
    packages=find_packages(),
    url='https://github.com/Bowowzahoya/lens_analysis',
    description='Analysis of Lens patent exports',
    long_description=open('README.text').read(),
    install_requires=[
        "pandas",
        ],
    include_package_data=True,
)