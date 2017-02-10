#!/bin/bash
cd $(dirname $0)
parallel --shuf python test.py "$*" ::: $(toe | cut -f 1) ::: --bytes --str
