from cm_api.api_client import ApiResource
cm_host = "cm-api-mn0.westus2.cloudapp.azure.com"
user = "cloudera"
password = "Cloudera_123"
api = ApiResource(cm_host, username=user, password=password)


def print_hosts(api):
    for h in api.get_all_hosts():
        print(h)


def print_clusters(api):
    for c in api.get_all_clusters():
        print c.name


def print_services(api):
    for c in api.get_all_clusters():
        for s in c.get_all_services():
            print "%s - %s  - %s" % (s.name, s.displayName, s.type)


def print_roles(api):
    for c in api.get_all_clusters():
        for s in c.get_all_services():
            if s.type == "KUDU":
                for r in s.get_all_roles():
                    print vars(r)


def print_kudu_configs(api):
    for c in api.get_all_clusters():
        for s in c.get_all_services():
            if s.type == "KUDU":
                for r in s.get_all_roles():
                    config = r.get_config(view='full')
                    print(config['fs_wal_dir'])
                    print(config['fs_data_dirs'])
                    print(config)


def print_kudu_role_group_configs(api):
    for c in api.get_all_clusters():
        for s in c.get_all_services():
            if s.type == "KUDU":
                for rcg in s.get_all_role_config_groups():
                    print "%s - %s" % (rcg.name, rcg.displayName)
                    for name, config in rcg.get_config(view='full').items():
                        print "%s - %s - %s" % (name, config.relatedName, config.description)


def create_kudu_roles(api):
    for c in api.get_all_clusters():
        for s in c.get_all_services():
            if s.type == "KUDU":
                i = 0
                for host in api.get_all_hosts():
                    if "-dn" in host.hostname:
                        try:
                            s.delete_role("KUDU_TSERVER_"+str(i))
                        except:
                            pass
                        r = s.create_role("KUDU_TSERVER_"+str(i),
                                          "KUDU_TSERVER", host.hostId)
                        i += 1
                    elif "-mn" in host.hostname:
                        try:
                            s.delete_role("KUDU_MASTER_0")
                        except:
                            pass
                        r = s.create_role("KUDU_MASTER_0",
                                          "KUDU_MASTER", host.hostId)


def add_kudu_service(api):
    for c in api.get_all_clusters():
        c.create_service("KUDU-1", "KUDU")


def delete_service(api, name):
    for c in api.get_all_clusters():
        try:
            c.delete_service(name)
        except:
            pass


def get_service_by_name(api, cluster_name, service_name):
    return api.get_cluster(cluster_name).get_service(service_name)


def print_role_types(api, cluster_name, service_name):
    for rt in get_service_by_name(api, cluster_name, service_name).get_role_types():
        print rt


def update_kudu_role_group_configs(api):
    for c in api.get_all_clusters():
        for s in c.get_all_services():
            if s.type == "KUDU":
                for rcg in s.get_all_role_config_groups():
                    if rcg.roleType == 'KUDU_MASTER':
                        rcg.update_config({"fs_wal_dir": "/data/master",
                                           "fs_data_dirs": "/data/master"})
                    elif rcg.roleType == 'KUDU_TSERVER':
                        rcg.update_config({"fs_wal_dir": "/data/tserver",
                                           "fs_data_dirs": "/data/tserver"})


def start_service(api, cluster, service):
    api.get_cluster(cluster).get_service(service).start()


print_services(api)
delete_service(api, "KUDU-1")
add_kudu_service(api)
create_kudu_roles(api)
update_kudu_role_group_configs(api)
start_service(api, "cm-api", "KUDU-1")
# print_role_types(api, "cm-api", "kudu")
print_roles(api)
print_kudu_configs(api)
print_kudu_role_group_configs(api)
