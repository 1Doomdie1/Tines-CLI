from setuptools import setup, find_packages

# Function to read requirements from requirements.txt
def load_requirements(filename="requirements.txt"):
    with open(filename, "r") as file:
        return file.read().splitlines()

setup(
    name="tines-cli",
    version="0.1",
    packages=find_packages(),
    py_modules=['tines'],
    install_requires=load_requirements(),
    entry_points={
        "console_scripts": [
            "tines=tines:app",
        ],
    },
)
