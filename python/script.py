# This is just a playground for experimenting with the cm api

from cm_api.api_client import ApiResource
cm_host = "cm-api5-mn0.westus2.cloudapp.azure.com"
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
        print "| service name | displayname | type |"
        print "|-"
        for s in c.get_all_services():

            print "|%s |  %s  | %s |" % (s.name, s.displayName, s.type)
        print "|-"


def print_roles_for_service_type(api, stype):
    for c in api.get_all_clusters():
        for s in c.get_all_services():
            if s.type == stype:
                for r in s.get_all_roles():
                    print
                    print r
                    print vars(r)


def print_role_configs_for_service_type(api, stype):
    for c in api.get_all_clusters():
        for s in c.get_all_services():
            if s.type == stype:
                for r in s.get_all_roles():
                    print
                    print r
                    print r.get_config()


def print_kudu_configs(api):
    for c in api.get_all_clusters():
        for s in c.get_all_services():
            if s.type == "KUDU":
                for r in s.get_all_roles():
                    config = r.get_config(view='full')
                    print(config['fs_wal_dir'])
                    print(config['fs_data_dirs'])
                    print(config)


def print_service_type_role_group_configs(api, stype):
    for c in api.get_all_clusters():
        for s in c.get_all_services():
            if s.type == stype:
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


def print_service_types(api):
    print
    print "Service Types"
    for t in api.get_all_clusters()[0].get_service_types():
        print t


def print_service_config_by_service_type(api, stype):
    print
    print "Service configs by service type"
    for s in api.get_all_clusters()[0].get_all_services(view='full'):
        if s.type == stype:
            print "name: %s displayName: %s" % (s.name, s.displayName)
            config = s.get_config()[0]
            print config


def print_impala_resource_configs(api, stype):
    for s in api.get_all_clusters()[0].get_all_services(view='full'):
        if s.type == stype:
            print "name: %s displayName: %s" % (s.name, s.displayName)
            config = s.get_config()[0]
            print config


for service in api.get_all_clusters()[0].get_all_services():
    print "** Service name:%s type: %s displayName: %s" % (service.name, service.type, service.displayName)
    config = service.get_config()
    print
    print "Service Config: %s" % str(config)
    print
    for rcg in service.get_all_role_config_groups():
        print "rcg name: %s rcg display name: %s" % (rcg.name, rcg.displayName)
        config = rcg.get_config()
        print
        print "rcg config: %s" % str(config)
    for role in service.get_all_roles():
        print
        print "role name: %s role type: %s" % (role.name, role.type)
        print
        print "role config: %s" % (role.get_config())


# print_services(api)
# print_service_types(api)
# for service in get_services_by_type(get_service_types):
#     print
# delete_service(api, "KUDU-1")
# add_kudu_service(api)
# create_kudu_roles(api)
# update_kudu_role_group_configs(api)
# start_service(api, "cm-api", "KUDU-1")
# print_role_types(api, "cm-api", "nifitoolkitca")
# print_roles(api)
# print_kudu_configs(api)
# print_service_type_role_group_configs(api, "IMPALA")
# print_service_config_by_service_type(api, "IMPALA")
# print_role_configs_for_service_type(api, "IMPALA")
