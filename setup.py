"""
Setup script for STRD Burn Monitor Discord Bot.

This script allows the bot to be installed as a Python package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="strd-burn-monitor",
    version="1.0.0",
    author="STRD Burn Monitor Team",
    author_email="team@stride.zone",
    description="A simple Discord bot that monitors STRD token burns from the Stride blockchain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/burnbot-discord",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "strd-burn-monitor=strd_burn_monitor:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 