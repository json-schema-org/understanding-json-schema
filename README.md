understanding-json-schema
=========================

A website aiming to provide more accessible documentation for JSON schema.

http://json-schema.org/understanding-json-schema/index.html

[![Build Status](https://travis-ci.org/json-schema-org/understanding-json-schema.png)](https://travis-ci.org/json-schema-org/understanding-json-schema)

# Building the docs
If you'd like to contribute to the docs, this is how you can build them on your own machine before submitting a PR.
## Docker
Build an image from the provided `Dockerfile`:
```
docker build -t undestanding-json-schema .
```
run a container from the built image to generate the docs:
```
docker run -it --rm -v $PWD:/doc undestanding-json-schema
```
After this you will find the generated docs inside the `build` folder.
