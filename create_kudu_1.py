import sys
from cm_api.api_client import ApiResource


def add_kudu_service(cluster, name):
    cluster.create_service(name, "KUDU")


def create_kudu_roles(cluster, hosts):
    for service in cluster.get_all_services():
        if service.type == "KUDU":
            i = 0
            for host in hosts:
                if "-dn" in host.hostname:
                    try:
                        service.delete_role("KUDU_TSERVER_"+str(i))
                    except Exception:
                        pass
                    r = service.create_role("KUDU_TSERVER_"+str(i),
                                            "KUDU_TSERVER", host.hostId)
                    i += 1
                elif "-mn" in host.hostname:
                    try:
                        service.delete_role("KUDU_MASTER_0")
                    except Exception:
                        pass
                    r = service.create_role("KUDU_MASTER_0",
                                            "KUDU_MASTER", host.hostId)


def update_kudu_role_group_configs(cluster):
    for service in cluster.get_all_services():
        if service.type == "KUDU":
            for rcg in service.get_all_role_config_groups():
                if rcg.roleType == 'KUDU_MASTER':
                    rcg.update_config({"fs_wal_dir": "/data/master",
                                       "fs_data_dirs": "/data/master"})
                elif rcg.roleType == 'KUDU_TSERVER':
                    rcg.update_config({"fs_wal_dir": "/data/tserver",
                                       "fs_data_dirs": "/data/tserver"})


def start_service(cluster, service_name):
    cmd = cluster.get_service(service_name).start()
    print "Waiting for %s to stop" % (service_name)
    cmd.wait()


def stop_service(cluster, service_name):
    try:
        cmd = cluster.get_service(service_name).stop()
        print "Waiting for %s to start" % (service_name)
        cmd.wait()
    except Exception:
        pass


service_name = "KUDU-1"


def main(cm_host, user, password):
    api = ApiResource(cm_host, username=user, password=password)
    cluster = api.get_all_clusters()[0]
    stop_service(cluster, service_name)
    try:
        print "deleting existing %s" % service_name
        cluster.delete_service(service_name)
    except Exception:
        pass
    add_kudu_service(cluster, service_name)
    create_kudu_roles(cluster, api.get_all_hosts())
    update_kudu_role_group_configs(cluster)
    start_service(cluster, service_name)


def usage(name):
    print """
Usage: %s host user password

Create the KUDU-1 service on the given host, using the given
CM user and password
""" % (name)


if __name__ == "__main__":
    if (len(sys.argv) < 3):
        usage(sys.argv[0])
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
