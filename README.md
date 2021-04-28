understanding-json-schema
=========================

A website aiming to provide more accessible documentation for JSON schema.

http://json-schema.org/understanding-json-schema/index.html

[![Build Status](https://travis-ci.org/json-schema-org/understanding-json-schema.png)](https://travis-ci.org/json-schema-org/understanding-json-schema)

# Build locally

You will need ruby, python, and pip.


We recommend you install and use rbenv to manage ruby.

Further information: https://github.com/rbenv/rbenv

We recommend you install and use pyenv to manage python.

Further information: https://realpython.com/intro-to-pyenv

We recommend you install and use pipenv to use pip.

Further information: https://pypi.org/project/pipenv/

Using these tools, you can have a virtual and managable environment for this project without interfering with other projects that require similar tooling.


Once all set up, clone this repository.

Run `$ pipenv sync` to install the required python dependencies via pip.

Next, run `$ make html` to build the HTML for the site.


Different commands and requirements are needed to build the PDF version of the site.
Additionally, you will need TexLive.

Instructions are only defined in this repository for installing TexLive on Linux based systes, which is used by our CI/CD process.

You may find the following commands work, but they are provided as is without any guarantee.

`$ bash -x ./install-texlive.sh`
`$ export PATH=$PWD/texlive/bin/x86_64-linux:$PATH`
`$ make html latexpdf && cp build/latex/*.pdf build/html`
