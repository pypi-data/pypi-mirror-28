from setuptools import setup, find_packages

setup(
    name='kcardum',
    version='0.2',
    description='A sample Python project',
    python_requires='>=3',
    packages=find_packages(),
    entry_points={
            'console_scripts': [
                'llama=main:hello',
            ],
        },
)
