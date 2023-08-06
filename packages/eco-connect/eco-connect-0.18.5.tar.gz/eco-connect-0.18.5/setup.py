from setuptools import setup, find_packages


def get_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name='eco-connect',
    version='0.18.5',
    description='Ecorithm\'s eco-connect ',
    license="Proprietary",
    python_requires='>=3.6',
    url='https://github.com/ecorithm/eco-connect',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=get_requirements()
)
