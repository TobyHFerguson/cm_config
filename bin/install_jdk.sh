#!/bin/bash -x
CM_URL=${1:?"No CM URL given"}
AUSER=${2:?"No admin user given"}

PREFIX=$(echo $CM_URL | sed -n 's/\(.*\)-[dm]n[0-2].*/\1/p')
DOMAIN=$(echo $CM_URL | sed -n 's/.*-[dm]n[0-2]\.\(.*\):.*/\1/p')

for host in mn0 dn{0..2}
do
    echo ssh ${AUSER:?}@${PREFIX}-${host}.${DOMAIN} 'sudo wget -P /etc/yum.repos.d/ https://archive.cloudera.com/director/redhat/7/x86_64/director/cloudera-director.repo && sudo yum -y install oracle-j2sdk1.8.x86_64'
done

echo ssh cloudera@${PREFIX}-mn0.${DOMAIN} 'echo export JAVA_HOME=/usr/java/jdk1.8.0_121-cloudera | sudo tee -a /etc/default/cloudera-scm-server'
    

