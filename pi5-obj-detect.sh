#!/bin/env bash

DIR=$(dirname $0)

echo "Making sure we are setup..."
$(${DIR}/setup.sh)
echo "Done with setup!"

echo "Starting application"
pushd ${DIR}
python main.py $1
popd
echo "Done!"