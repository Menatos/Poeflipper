#!/bin/bash

set -e

RELEASE_BRANCH='release-1.0_3.24'

echo "Stopping all running python processes"
pkill -9 -f "python"
echo "Python processes stopped"

echo "Fetching Poeflipper repository"
git fetch
echo "Poeflipper repository fetched"

echo "Checkout release branch"
git checkout ${RELEASE_BRANCH}
echo "Checked out release branch"

echo "Pulling release branch"
git pull
echo "Pulled release branch"

echo "Executing run.sh to start processes"
sudo bash run.sh
echo "run.sh started"

echo "Script successfully completed"
echo "---- HAVE A NICE DAY ----"