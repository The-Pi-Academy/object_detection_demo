#!/bin/env bash

DIR=$(dirname $0)

echo "Making sure we are setup..."
$(${DIR}/setup.sh)
echo "Done with setup!"

echo "Starting application"
pushd ${DIR}
source ./.venv/bin/activate
python main.py $1
deactivate
popd
echo "Done!"