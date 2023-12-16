from setuptools import setup, find_packages

setup(
    name='londontube',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'londontube_journey_planner = londontube.journey_planner:journey_planner',
        ],
    },
)