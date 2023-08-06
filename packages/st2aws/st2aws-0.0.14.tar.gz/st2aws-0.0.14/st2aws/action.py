import re
import json
import boto3
import importlib

from st2actions.runners.pythonrunner import Action
from parsers import ResultSets
from datetime import datetime


class BaseAction(Action):

    def __init__(self, config):
        super(BaseAction, self).__init__(config)

        self.credentials = {
            'region': None,
            'aws_access_key_id': None,
            'aws_secret_access_key': None
        }
        self.userdata = None

        if config.get('st2_user_data', None):
            try:
                with open(config['st2_user_data'], 'r') as fp:
                    self.userdata = fp.read()
            except IOError as e:
                self.logger.error(e)

        # Note: In old static config credentials and region are under "setup" key and with a new
        # dynamic config values are top-level
        access_key_id = config.get('aws_access_key_id', None)
        secret_access_key = config.get('aws_secret_access_key', None)
        region = config.get('region', None)

        if access_key_id == "None":
            access_key_id = None
        if secret_access_key == "None":
            secret_access_key = None

        if access_key_id and secret_access_key:
            self.credentials['aws_access_key_id'] = access_key_id
            self.credentials['aws_secret_access_key'] = secret_access_key
            self.credentials['region'] = region
        elif 'setup' in config:
            # Assume old-style config
            self.credentials = config['setup']

        if region:
            self.credentials['region'] = region

        self.resultsets = ResultSets()

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")

    def st2_user_data(self):
        return self.userdata

    def get_boto3_session(self, resource):
        region = self.credentials['region']
        del self.credentials['region']
        return boto3.client(resource, region_name=region, **self.credentials)

    def split_tags(self, tags):
        tag_dict = {}
        split_tags = tags.split(',')
        for tag in split_tags:
            if re.search('=', tag):
                k, v = tag.split('=', 1)
                tag_dict[k] = v
        return tag_dict

    def do_method(self, module_path, cls, action, **kwargs):
        module = importlib.import_module(module_path)
        if 'boto3' in module_path:
            for k, v in kwargs.items():
                if not v:
                    del kwargs[k]
            obj = self.get_boto3_session(cls)
        else:
            del self.credentials['region']
            obj = getattr(module, cls)(**self.credentials)

        if not obj:
            raise ValueError('Invalid or missing credentials (aws_access_key_id,'
                             'aws_secret_access_key) or region')

        resultset = getattr(obj, action)(**kwargs)
        formatted = self.resultsets.formatter(resultset)
        return formatted

    def do_function(self, module_path, action, **kwargs):
        module = __import__(module_path)
        return getattr(module, action)(**kwargs)
