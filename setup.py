"""
AfriLang Python SDK – setup.py

Install locally:   pip install -e sdk/
Publish to PyPI:   python -m build sdk/ && twine upload dist/*
"""
from setuptools import setup, find_packages

setup(
    name="afrilang",
    version="1.0.0",
    description="Official Python SDK for the AfriLang African language translation API",
    long_description=open("sdk/README_SDK.md").read(),
    long_description_content_type="text/markdown",
    author="AfriLang",
    url="https://github.com/umarkhemis/afrilang",
    license="MIT",
    package_dir={"": "sdk"},
    packages=find_packages(where="sdk"),
    python_requires=">=3.9",
    install_requires=[
        "httpx>=0.27.0",
    ],
    extras_require={
        "async": ["httpx>=0.27.0"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    keywords="african languages translation nlp swahili yoruba luganda sunbird",
)
