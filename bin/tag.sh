RESOURCE_GROUP=${1:?"No Resource Group specified"}
az group update -n "${RESOURCE_GROUP}" --set tags.owner=toby tags.purpose=testing tags.end_date='6/1/2019'

jsontag=$(az group show -n "${RESOURCE_GROUP}" --query tags)
t=$(echo $jsontag | tr -d '"{},' | sed 's/: /=/g')
r=$(az resource list -g ${RESOURCE_GROUP} --query [].id --output tsv)
for resid in $r
do
    az resource tag --tags $t --id $resid
done
