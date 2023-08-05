from setuptools import setup

with open("README.md") as f:
    long_desc = f.read()

setup(
    name="eve-cli-client",
    version="0.0.1b1",
    description="A basic cli client for testing eve-assistant without entering an API key.",
    long_description=long_desc,
    author="Karl Voss",
    author_email="karl.p.voss@gmail.com",
    license="MIT",
    packages=["eve_cli_client"],
    install_requires=[
        "requests"
    ]
)
