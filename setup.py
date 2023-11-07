from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = [
        line
        for line in (item.strip() for item in fh)
        if line and line[:1] not in ("#", "-")
    ]

setup(
    name="smsdk",
    version="1.0.24",
    packages=find_packages(exclude=["test*"]),
    include_package_data=True,
    install_requires=install_requires,
    license="",
    long_description=long_description,
    author="Sight Machine",
    author_email="support@sightmachine.com",
    url="http://sightmachine.com/",
    description="Sight Machine SDK",
    python_requires=">=3.8",
)
