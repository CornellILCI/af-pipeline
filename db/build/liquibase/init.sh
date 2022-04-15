#!/usr/bin/env bash
./liquibase --defaultsFile=liquibase-afdb.properties --username=${POSTGRES_USER} --password=${POSTGRES_PASSWORD} update
