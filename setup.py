from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    "numpy==1.18.4",
    "requests==2.24.0",
    "pytest==6.0.2",
    #"pandas==0.23.4",
    "mock==4.0.2",
    "importlib-resources==3.0.0"
]

setup(
    name="smsdk",
    version="1.0",
    packages=find_packages(exclude=["test*"]),
    include_package_data=True,
    install_requires=install_requires,
    license="",
    long_description=long_description,
    author="Sight Machine",
    author_email="support@sightmachine.com",
    url="http://sightmachine.com/",
    description="AI Data Pipeline tool",
    python_requires=">=3.6.8",
)
