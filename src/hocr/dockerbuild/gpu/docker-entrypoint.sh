#!/bin/bash

WORK_DIR=$1

CMD=${@:2}
# Run CMD from $WORKDIR
bash -c "cd $WORK_DIR && $CMD"