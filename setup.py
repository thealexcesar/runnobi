from setuptools import setup, find_packages

setup(
    name="runnobi",
    version="1.0.0",
    description="Fast-paced ninja endless runner with parkour and combat mechanics",
    author="thealexcesar",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.5.2",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "runnobi=runnobi.main:main",
        ],
    },
)
