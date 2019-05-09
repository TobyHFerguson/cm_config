import sys
from cm_api.api_client import ApiResource


def main(cm_host, user, password):
    api = ApiResource(cm_host, username=user, password=password)
    cm = api.get_cloudera_manager()
    cm.update_all_hosts_config(
        {"java_home": "/usr/java/jdk1.8.0_121-cloudera"})
    print("restarting CM service - this will take a minute or so")
    cm.get_service().restart().wait()
    print("restarting cluster - this will take 2-5 minutes")
    api.get_all_clusters()[0].restart(restart_only_stale_services=True,
                                      redeploy_client_configuration=True).wait()


def usage(name):
    print """
Usage: %s host user password

Configure JDK 1.8 for each host in the cluster managed by ClouderaManager
running on host, using the user/password credentials
""" % (name)


if __name__ == "__main__":
    if (len(sys.argv) < 3):
        usage(sys.argv[0])
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
