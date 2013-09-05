#!/bin/bash

# Stop at the first error
set -e

GH_ACCOUNT=spacetelescope
GH_REPOSITORY=understanding-json-schema
GH_REMOTE=live
GH_PAGESBRANCH=gh-pages

function error_exit
{
	echo -e "\e[01;31m$1\e[00m" 1>&2
	exit 1
}

if [ "$TRAVIS_PULL_REQUEST" = "false" ]; then
	git remote add $GH_REMOTE https://${GH_TOKEN}@github.com/$GH_ACCOUNT/$GH_REPOSITORY.git

	git config --global user.email ${GH_EMAIL}
        git config --global user.name "Michael Droettboom"

	git checkout --orphan $GH_PAGESBRANCH

        # This will delete all of the git-managed files here, but not
        # the results of the build
        git rm -rf .
        cp -r build/html/* .
        git add *
        git commit -m "Generated from sources"

	echo "Push to gh-pages branch"
	git push -f $GH_REMOTE $GH_PAGESBRANCH
fi
