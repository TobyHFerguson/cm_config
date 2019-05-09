CM_URL=${1:?"No CM URL given"}
USER=${2:?"No admin user given"}
PATH=$(dirname $0):$PATH
install_jdk.sh ${PREFIX:?}
install_csds.sh ${CM_URL?} ${USER:?}
