#!/bin/env bash

pushd $(dirname $0)

echo "Beginning setup."

if [[ ! -d ".venv" ]]
then
  python -mvenv .venv
fi

source .venv/bin/activate
pip install --upgrade pip
pip install --upgrade -r requirements.txt
deactivate
echo "Setup completed!!!"

popd


