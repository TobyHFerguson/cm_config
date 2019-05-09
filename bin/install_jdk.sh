#!/bin/bash -x
PREFIX=${1:?No prefix given}
DOMAIN=westus2.cloudapp.azure.com
for host in mn0 dn{0..2}
do
    ssh cloudera@${PREFIX}-${host}.${DOMAIN} 'sudo wget -P /etc/yum.repos.d/ https://archive.cloudera.com/director/redhat/7/x86_64/director/cloudera-director.repo && sudo yum -y install oracle-j2sdk1.8.x86_64'
done

ssh cloudera@${PREFIX}-mn0.${DOMAIN} 'echo export JAVA_HOME=/usr/java/jdk1.8.0_121-cloudera | sudo tee -a /etc/default/cloudera-scm-server'
    

