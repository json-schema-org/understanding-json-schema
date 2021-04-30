FROM fedora

# Install texlive
RUN dnf update -y
RUN dnf install -y make latexmk texlive
RUN dnf install -y 'tex(fncychap.sty)' \
                   'tex(tabulary.sty)' \
                   'tex(framed.sty)' \
                   'tex(wrapfig.sty)' \
                   'tex(upquote.sty)' \
                   'tex(capt-of.sty)' \
                   'tex(needspace.sty)' \
                   'tex(overlock.sty)' \
                   'tex(inconsolata.sty)' \
                   'tex(bbding.sty)' \
                   'tex(mdframed.sty)' \
                   'tex(bbding10.pfb)'
RUN texhash

# Install sphinx
RUN pip install "sphinx<2.0.0" sphinx-bootstrap-theme jsonschema

COPY . /code
WORKDIR /code

# Build and serve website
CMD make html latexpdf && cp build/latex/*.pdf build/html && python3 -m http.server 8000 --directory build/html
