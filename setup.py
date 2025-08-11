from setuptools import setup, find_packages

setup(
    name="stratified-shuffle",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.32.0",
        "python-dotenv>=1.0.1",
        "pandas>=2.2.1",
        "numpy>=1.26.4",
    ],
    python_requires=">=3.8",
) 