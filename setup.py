import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sphinx_graphiql",
    version="0.0.1",
    author="Rikin K",
    author_email="rikin@hasura.io",
    description="Sphinx extension for GraphiQL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hasura/sphinx_graphiql",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
