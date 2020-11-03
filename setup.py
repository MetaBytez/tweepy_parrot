import setuptools


with open("README.md", "r") as f:
    long_description = f.read()


setuptools.setup(
    name="tweepy-parrot",
    version="0.0.2",
    author="Will Johns",
    author_email="will@wcj.dev",
    description="A library built on top of Tweepy for making Twitter bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MetaBytez/tweepy_parrot",
    packages=setuptools.find_packages(),
    install_requires=[
        'tweepy',
        'pydantic',
        'python-dotenv'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
