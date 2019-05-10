#!/bin/sh
if [ $# -ne 3 ]
then
    cat <<EOF
Expected 3 arguments, got $#

CM_URL CM_username CM_password

EOF
URL=${1:?No URL to the Cloudera Manager was given}
USER=${2:?No CM user name was given}
PASSWORD=${3:?No password provided}

HOST=$(echo ${URL#*://} | sed -n 's/\(.*\):*.*/\1/p')

for p in configure_jdk.py create_kudu_1.py create_nifi.py
do
    python /${p} ${HOST} ${USER:?} ${PASSWORD:?}
done
