from setuptools import setup

setup(
    name='kcardum',
    version='0.1',
    description='A sample Python project',
    python_requires='>=3',
    entry_points={
            'console_scripts': [
                'llama=main:hello',
            ],
        },
)
