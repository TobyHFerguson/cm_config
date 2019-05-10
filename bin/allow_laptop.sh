RESOURCE_GROUP=toby-cm-api7
PREFIX=cm-api7
for NSG in clouderaVnet-sg ${PREFIX}-dn-sg ${PREFIX}-mn-sg
do
    az network nsg rule create --name cloudera_vpn --nsg-name $NSG --priority 120 --access Allow --destination-address-prefixes '*' --destination-port-ranges '*' --direction Inbound --protocol '*' --source-address-prefixes 74.217.76.96/27 --resource-group ${RESOURCE_GROUP}
done
