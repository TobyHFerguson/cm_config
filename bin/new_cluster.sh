PREFIX=${1:?"No hostname prefix given"}
PATH=$(dirname $0):$PATH
install_jdk.sh ${PREFIX:?}
install_csds.sh ${PREFIX:?}
