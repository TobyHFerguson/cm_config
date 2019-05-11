RESOURCE_GROUP=${1:?"No Resource Group specified"}
CM_URL=${2:?"No CM URL specified"}

PREFIX=$(echo ${CM_URL#*://} | sed -n 's/\(.*\)-[dm]n[0-2].*/\1/p')

for NSG in clouderaVnet-sg ${PREFIX}-dn-sg ${PREFIX}-mn-sg
do
    az network nsg rule create --name cloudera_vpn --nsg-name $NSG --priority 120 --access Allow --destination-address-prefixes '*' --destination-port-ranges '*' --direction Inbound --protocol '*' --source-address-prefixes 74.217.76.96/27 --resource-group ${RESOURCE_GROUP}
done
