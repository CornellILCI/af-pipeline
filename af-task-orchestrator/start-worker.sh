#!/bin/sh

# Activate asreml license
echo $ASREML_ACTIVATION_CODE
asreml -z $ASREML_ACTIVATION_CODE


supervisord -c supervisord.cfg
