#!/bin/sh

rm db/tourbillon.db config/tourbillon.yaml
pipenv run site -s

