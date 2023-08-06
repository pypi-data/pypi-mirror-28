from setuptools import setup, find_packages

setup(
    name='dictionaryutils',
    version='1.2.0',
    packages=find_packages(),
    install_requires=[
        'PyYAML==3.11',
        'jsonschema==2.5.1',
    ],
    package_data={
        "dictionaryutils": [
            "schemas/*.yaml",
        ]
    },
)
