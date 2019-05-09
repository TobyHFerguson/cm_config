PREFIX=${1:?No prefix given}
DOMAIN=westus2.cloudapp.azure.com
ssh cloudera@${PREFIX}-mn0.${DOMAIN} 'jars=(http://archive.cloudera.com/CFM/csd/1.0.0.0/NIFI-1.9.0.1.0.0.0-90.jar http://archive.cloudera.com/CFM/csd/1.0.0.0/NIFICA-1.9.0.1.0.0.0-90.jar http://archive.cloudera.com/CFM/csd/1.0.0.0/NIFIREGISTRY-0.3.0.1.0.0.0-90.jar)
sudo wget -P /opt/cloudera/csd/ ${jars[*]}
sudo chown cloudera-scm:cloudera-scm /opt/cloudera/csd/NIFI*
sudo chmod 644 /opt/cloudera/csd/NIFI*
sudo systemctl restart cloudera-scm-server'
