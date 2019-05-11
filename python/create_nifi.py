import sys
import time
from cm_api.api_client import (ApiResource, ApiException)


def download_parcel(cluster, parcel):
    version = parcel.version
    print "Downloading %s parcel, version %s" % (parcel.product, version)
    parcel.start_download()
    while True:
        parcel = cluster.get_parcel('CFM', version)
        if parcel.stage == 'DOWNLOADED':
            break
        if parcel.state.errors:
            raise Exception(str(parcel.state.errors))
        print "download progress: %s / %s" % (parcel.state.progress,
                                              parcel.state.totalProgress)
        time.sleep(15)  # check again in 15 seconds
    print "downloaded %s parcel version %s on cluster %s" % (parcel.product,
                                                             version, cluster)


def distribute_parcel(cluster, parcel):
    version = parcel.version
    print "Distributing %s parcel, version %s" % (parcel.product, version)
    parcel.start_distribution()
    while True:
        parcel = cluster.get_parcel('CFM', version)
        if parcel.stage == 'DISTRIBUTED':
            break
        if parcel.state.errors:
            raise Exception(str(parcel.state.errors))
        print "Distribution progress: %s / %s" % (parcel.state.progress,
                                                  parcel.state.totalProgress)
        time.sleep(15)  # check again in 15 seconds
    print "distributed %s parcel version %s on cluster %s" % (parcel.product,
                                                              version, cluster)


def restart_cluster(cluster):
    print "Restarting cluster %s" % (cluster.name)
    cluster.restart().wait()
    print "Cluster %s restarted" % (cluster.name)


def print_nifi_ca_roles(cluster):
    for s in cluster.get_all_services():
        if s.type == "NIFITOOLKITCA":
            for r in s.get_all_roles():
                print vars(r)


def print_nifi_role_group_configs(cluster):
    for s in cluster.get_all_services():
        if s.type == "NIFITOOLKITCA":
            for rcg in s.get_all_role_config_groups():
                print
                print "%s - %s" % (rcg.name, rcg.displayName)
                for name, config in rcg.get_config(view='full').items():
                    print "%s - %s - %s" % (name, config.relatedName, config.description)


def create_nifi_ca_roles(cluster, hosts):
    for service in cluster.get_all_services():
        if service.type == "NIFITOOLKITCA":
            for host in hosts:
                if "-dn0" in host.hostname:
                    role_name = "NiFi Toolkit"
                    try:
                        service.delete_role(role_name)
                    except Exception:
                        pass
                    r = service.create_role(role_name, "NIFI_TOOLKIT_SERVER")


def ensure_CFM_parcel_is_activated(api):
    print "Ensuring CFM parcel is activated"
    cluster = api.get_all_clusters()[0]
    parcel_repo = 'http://archive.cloudera.com/CFM/parcels/1.0.0.0/'
    cm_config = api.get_cloudera_manager().get_config(view='full')
    repo_config = cm_config['REMOTE_PARCEL_REPO_URLS']
    value = repo_config.value or repo_config.default
    # value is a comma-separated list
    if parcel_repo in value:
        print "%s already configured - skipping" % parcel_repo
    else:
        value += ',' + parcel_repo
        api.get_cloudera_manager().update_config({
            'REMOTE_PARCEL_REPO_URLS': value})
        # wait to make sure parcels are refreshed
        time.sleep(10)

    for parcel in cluster.get_all_parcels():
        #        print "%s - %s" % (parcel.product, parcel.stage)
        if parcel.product == "CFM":
            if parcel.stage == "AVAILABLE_REMOTELY":
                download_parcel(cluster, parcel)
                distribute_parcel(cluster, parcel)
                parcel.activate()
                restart_cluster(cluster)
            elif parcel.stage == "DOWNLOADED":
                distribute_parcel(cluster, parcel)
                parcel.activate()
                restart_cluster(cluster)
            elif parcel.stage == "DISTRIBUTED":
                parcel.activate()
                restart_cluster(cluster)
            elif parcel.stage == "ACTIVATED":
                pass


def main(cm_host, user, password):
    api = ApiResource(cm_host, username=user, password=password)

    ensure_CFM_parcel_is_activated(api)

    create_nifi_toolkit_ca(api)

    create_nifi_registry(api)

    create_nifi(api)


def create_nifi_toolkit_ca(api):
    cluster = api.get_all_clusters()[0]

    service_name = "nifitoolkitca"
    service_type = "NIFITOOLKITCA"
    role_name = "NiFi_Toolkit_role_name"
    role_type = "NIFI_TOOLKIT_SERVER"

    try:
        cluster.get_service(service_name)
        print "Service %s already configured. Skipping" % service_name
    except ApiException:
        print "Creating NIFI Tookit CA"
        n = cluster.create_service(service_name, service_type)
        n.update_config(
            {"nifi.toolkit.tls.ca.server.token": "ClouderaNifi_123"})
        n.displayName = "NiFi Toolkit CA Service"
    #    print "%s - %s - %s" % (n.name, n.type, n.displayName)

        for host in api.get_all_hosts():
            if "-dn0" in host.hostname:
                n.create_role(role_name, role_type, host.hostname)

        # n.deploy_client_config(role_name).wait()
        n.start().wait()


def create_nifi_registry(api):
    cluster = api.get_all_clusters()[0]
    service_name = "nifiregistry"
    service_type = "NIFIREGISTRY"
    service_displayName = "NiFi Registry"
    role_name = "nifiregistry"
    role_type = "NIFI_REGISTRY_SERVER"

    try:
        cluster.get_service(service_name)
        print "Service %s already configured. Skipping" % service_name
    except ApiException:
        print "Creating NIFI Registry"
        n = cluster.create_service(service_name, service_type)
        n.__class__.displayName = service_displayName
        n.update_config({"nifitoolkitca_service": "nifitoolkitca"})
        for host in api.get_all_hosts():
            if "-dn0" in host.hostname:
                n.create_role(role_name, role_type, host.hostname)

        n.start().wait()


def create_nifi(api):
    cluster = api.get_all_clusters()[0]
    service_name = "nifi"
    role_name = "nifi"

    try:
        cluster.get_service(service_name)
        print "Service %s already configured. Skipping" % service_name
    except ApiException:
        print "(Re)creating NiFi"
        n = cluster.create_service(service_name, "NIFI")
        n.displayName = "NiFi"
        n.update_config({"zookeeper_service": "zookeeper",
                         "nifitoolkitca_service": "nifitoolkitca"})

        for host in api.get_all_hosts():
            if "-dn0" in host.hostname:
                n.create_role(role_name, "NIFI_NODE", host.hostname)

        n.start().wait()


def usage(name):
    print """
Usage: %s host user password

Create the NIFI services on the given host, using the given
CM user and password
""" % (name)


if __name__ == "__main__":
    if (len(sys.argv) < 3):
        usage(sys.argv[0])
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
