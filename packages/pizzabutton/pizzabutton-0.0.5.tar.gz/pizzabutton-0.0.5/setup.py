from setuptools import setup, find_packages

try:
    long_desc = open('README.md').read()
except:
    long_desc = ''

setup(
    name="pizzabutton",
    url="https://github.com/peterskipper/pizzabutton",
    author="Peter Skipper",
    author_email="peter.skipper@gmail.com",
    version="0.0.5",
    packages=find_packages(),
    install_requires=[
        "pizzapi==0.0.3",
        "jupyter==1"
    ],
    #package_data={
    #    "pizzabutton": ["static/index.js"]
    #},
    include_package_data=True,
    description="A button on Jupyter's toolbar for pizza",
    long_description=long_desc,
)
