#!/bin/sh

make html latexpdf
cp build/latex/*.pdf build/html
exec "$@"
