#!/usr/bin/env bash
./wait-for-it.sh database:5432 -- ./init.sh