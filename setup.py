"""Setup script."""
import DNSoverTLS
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

_version = DNSoverTLS.__version__
_requires = open("requirements.txt").read().splitlines()

setuptools.setup(
    name="DockerENT",
    version=_version,
    description="A simple proxy server to convert DNS Requests to DNS-over-TLS using Cloudflare",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=_requires,
    entry_points={"console_scripts": {
        "DNSoverTLS = DNSoverTLS.__main__:start"}},
    keywords="DNS DNS-over-TLS TLS cloudflare",
)
