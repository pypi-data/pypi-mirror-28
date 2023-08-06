from .client import CLIENT_MAP
from .errors import StoneKeyError


class Cluster(object):
    """
    Cluster Info.
    """

    def __init__(self, cluster_type):
        self.cluster_type = cluster_type

        self.cluster_url = None
        self.cluster_username = None
        self.cluster_password = None

        self.cluster_env = None

    def set_connect(self, cluster_url, cluster_username, cluster_password):
        self.cluster_url = cluster_url
        self.cluster_username = cluster_username
        self.cluster_password = cluster_password

    def set_env_label(self, env_label):
        self.cluster_env = env_label


class MicroServices(object):
    """
    MicroServices Info.
    """

    def __init__(self, ms_id, package_type):
        self.ms_id = ms_id
        self.package_type = package_type
        self.package_name = None
        self.release_name = None

        self.release_path = None
        self.token = None

    def set_package_info(self, package_name, release_name):
        self.package_name = package_name
        self.release_name = release_name

    def set_release_path(self, release_path, token):
        self.release_path = release_path
        self.token = token


class TaskStone(object):
    def __init__(self, cluster, micro_services, report):
        self.cluster = cluster
        self.micro_services = micro_services
        self.report = report
        self.logger = None
        self._result = {}
        self._stone = {
            'config': {},
            'result': {}
        }

    @property
    def client(self):
        client_cls = CLIENT_MAP[self.client.cluster_type]
        client = client_cls(self.client)
        client.login()
        return client

    def set_config(self, key, value):
        self._stone['config'][key] = value

    def get_config(self, key, default=None):
        self._stone['config'].get(key, default=default)

    def set_result(self, func_name, result):
        self._result[func_name] = result

    def get_result(self, func_name, default=None):
        self._result[func_name].get(func_name, default=default)

    def set_value(self, key, value):
        if key in ['cluster', 'micro_services', 'config', 'result']:
            raise StoneKeyError("不能使用 {} 作为 key。".format(key))
        self._stone[key] = value

    def get_value(self, key, default=None):
        return self._stone.get(key, default=default)
