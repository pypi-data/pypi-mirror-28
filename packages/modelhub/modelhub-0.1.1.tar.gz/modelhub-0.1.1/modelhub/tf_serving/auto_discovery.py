# encoding=utf8
# author=spenly
# mail=i@spenly.com

from redis import StrictRedis


class AutoDiscovery(object):

    def __init__(self, center_host, center_port):
        self._redis = StrictRedis(host=center_host, port=center_port)

    def register(self, model_name, hostport, version=None, timeout=10):
        """
        register a TF serving info
        :param model_name: model name
        :param version: model version
        :param timeout: expire time
        :return:
        """
        self._redis.set(model_name, value=hostport, ex=timeout)

    def get_host_port(self, model_name, version=None):
        """
        get a TF serving host info
        :param model_name:
        :param version:
        :return:
        """
        return self._redis.get(model_name)

