from setuptools import setup, find_packages

setup(
    name='londontube',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'requests',
        'datetime',
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'journey-planner = londontube.journey_planner:process',
        ],
    },
)