#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="alerttime-xss-scanner",
    version="2.5.0",
    author="Orkhan Khalafi",
    author_email="contact@orkhankhalafi.com",
    description="Advanced Multi-threaded XSS Vulnerability Scanner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orkhankhalafi/alerttime-xss-scanner",
    project_urls={
        "Bug Tracker": "https://github.com/orkhankhalafi/alerttime-xss-scanner/issues",
        "Documentation": "https://github.com/orkhankhalafi/alerttime-xss-scanner#readme",
        "Source Code": "https://github.com/orkhankhalafi/alerttime-xss-scanner",
        "Author LinkedIn": "https://www.linkedin.com/in/orkhankhalafi/",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Networking :: Monitoring",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "alerttime=alerttime:main",
        ],
    },
    keywords=[
        "xss", "security", "vulnerability", "scanner", "penetration-testing",
        "web-security", "ethical-hacking", "security-testing", "waf-bypass",
        "multi-threading", "professional", "reporting"
    ],
    include_package_data=True,
    zip_safe=False,
)