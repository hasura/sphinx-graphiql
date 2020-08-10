import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ontotext_sphinx_graphiql",
    version="0.0.4",
    author="Jem Rayfield",
    author_email="jem.rayfield@ontotext.com",
    description="Sphinx extension for GraphiQL, from Hasura, patched for Ontotext",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jazzyray/sphinx-graphiql",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
         