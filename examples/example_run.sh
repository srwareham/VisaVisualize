#!/usr/bin/env bash

# Great one liner sourced from https://stackoverflow.com/questions/59895/
THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT=$(dirname "$THIS_DIR")
cd "$PROJECT_ROOT"

###### START RELEVANT SCRIPT ######

# Change example name to any example script name
exampleName="contrib_by_county_and_state"

echo Running script: \""$exampleName"\"...
python -m examples."$exampleName"