PREFIX=cm-api7
RESOURCE_GROUP=toby-cm-api7
IP=$(curl ifconfig.me)
SUBS=$(az account show | jq -r '.id')
for name in clouderaVnet-sg ${PREFIX}-dn-sg ${PREFIX}-mn-sg
do
    az network nsg rule create --name laptop --nsg-name $name --resource-group ${RESOURCE_GROUP} --priority 110 --access Allow --destination-address-prefixes '*' --destination-port-ranges '*' --direction Inbound --protocol '*' --source-address-prefixes $IP --subscription $SUBS
done
