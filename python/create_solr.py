import sys
from cm_api.api_client import ApiResource


def create_solr(api):
    cluster = api.get_all_clusters()[0]
    service_name = "solr"
    service_type = "SOLR"
    service_displayName = "Solr"
    rcg_name = "solr-SOLR_SERVER-BASE"
    rcg_config = {u'solr_java_direct_memory_size': u'268435456',
                  u'solr_java_heapsize': u'209715200'}
    role_name = "solr"
    role_type = "SOLR_SERVER"

    try:
        cluster.delete_service(service_name)
    except Exception:
        pass

    solr_service = cluster.create_service(service_name, service_type)
    solr_service.__class__.displayName = service_displayName
    solr_service.update_config({u'zookeeper_service': u'zookeeper',
                                u'hdfs_service': u'hdfs'})
    rcg = solr_service.get_role_config_group(rcg_name)
    rcg.update_config(rcg_config)
    solr_service.update_role_config_group(rcg_name, rcg)
    for host in api.get_all_hosts():
        if "-dn1" in host.hostname:
            role = solr_service.create_role(
                role_name, role_type, host.hostname)

    print "Waiting for service %s to start" % service_name
    solr_service.start().wait()
    print "Service %s has started" % service_name


def main(cm_host, user, password):
    api = ApiResource(cm_host, username=user, password=password)

    create_solr(api)


def usage(name):
    print """
Usage: %s host user password

Create the SOLR service on the given host, using the given
CM user and password
""" % (name)


if __name__ == "__main__":
    if (len(sys.argv) < 3):
        usage(sys.argv[0])
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
