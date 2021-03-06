URL=${1:?No URL to the Cloudera Manager was given}
USER=${2:?No CM user name was given}
PASSWORD=${3:?No password provided}

HOST=$(echo ${URL#*://} | sed -n 's/\(.*\):*.*/\1/p')

for p in configure_jdk.py create_kudu_1.py create_nifi.py
do
    docker run --rm -i -t tobyhferguson/cm_config python /${p} ${HOST} ${USER:?} ${PASSWORD:?}
done
