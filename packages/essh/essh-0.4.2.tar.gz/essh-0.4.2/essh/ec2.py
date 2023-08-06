from os import environ
from os.path import abspath, dirname, join, isfile
import logging
import boto3
import botocore
from time import sleep
import time, datetime
from retrying import retry
from pprint import pprint
from os import environ
from essh.exceptions import ESSHException
import re

class Instance(object):
    def __init__(self, instance_id, private_ip, keypair):
        self.instance_id = instance_id
        self.private_ip = private_ip
        self.keypair = keypair

class EC2Controller(object):
    def __init__(self, profile_name, zone):
        self.instance_id_regex = re.compile('^i-')
        self.ip_regex = re.compile('^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
        self.api = EC2(profile_name=profile_name, zone=zone)

    def find(self, target):
        if re.search(self.instance_id_regex, target) is not None:
            return self.api.find_by_id(target)
        elif re.search(self.ip_regex, target) is not None:
            return self.api.find_by_ip(target)
        else:
            return self.api.find_by_name(target)
class EC2(object):
    def __init__(self, ec2_client=None, profile_name=None, zone=None):
        logging.basicConfig(level=logging.ERROR)
        self.logger = logging.getLogger(__name__)
        self.ec2 = ec2_client or self._get_ec2_client(profile_name, zone)
        self.array_regex = re.compile('\[([0-9]+)\]$')
        self.zone = zone

    def _require_env_var(self, key):
        if key not in environ:
            raise ESSHException('Missing %s environment variable' % key)
        return environ[key]

    def _get_ec2_client(self, profile_name, zone):
        if profile_name:
            session = boto3.Session(profile_name=profile_name)
            if zone:
                return session.client('ec2', region_name=zone[:-1])
            else:
                return session.client('ec2')
        else:
            kwargs = {
                'aws_access_key_id': self._require_env_var('AWS_ACCESS_KEY_ID'),
                'aws_secret_access_key': self._require_env_var('AWS_SECRET_ACCESS_KEY'),
                'region_name': environ.get('AWS_REGION', 'us-east-1')
            }

            if environ.get('AWS_SESSION_TOKEN'):
                kwargs['aws_session_token'] = environ.get('AWS_SESSION_TOKEN')

            return boto3.client('ec2', **kwargs)

    def find_by_name(self, name):
        name, index = self._extra_index(name)

        filters = [
            {"Name": "instance-state-name", "Values": ["running"]},
            {"Name": "tag:Name", "Values": [name]}
        ]
        message = 'with name %s' % name
        if self.zone:
            filters.append({"Name": "availability-zone", "Values": [self.zone]})
            message += ' in zone %s' % self.zone

        return self._find(filters, message, index)

    def _extra_index(self, name):
        index = 0
        match = re.findall(self.array_regex, name)
        if len(match) > 0:
            name = name.split("[", 1)[0]
            index = int(match[0][0])

        return name, index

    def find_by_id(self, id):
        filters = [
            {"Name": "instance-state-name", "Values": ["running"]},
            {"Name": "instance-id", "Values": [id]}
        ]
        return self._find(filters, 'with id %s' % id)

    def find_by_ip(self, private_ip):
        filters = [
            {"Name": "instance-state-name", "Values": ["running"]},
            {"Name": "private-ip-address", "Values": [private_ip]}
        ]
        return self._find(filters, 'with private ip %s' % private_ip)

    def _find(self, filters, message, index=0):
        instance_id, keypair, private_ip = self._find_by_index(filters, index)
        if keypair and instance_id and private_ip:
            return Instance(instance_id, private_ip, keypair)
        else:
            raise ESSHException('No instance found %s' % message)

    def _find_by_index(self, filters, index=0):
        instance_id = None
        keypair = None
        private_ip = None

        instances = self._ec2_describe_instances(Filters=filters)
        for reservation in instances.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                if 'InstanceId' in instance:
                    instance_id = instance['InstanceId']
                    keypair = instance['KeyName']
                    private_ip = instance['PrivateIpAddress']
                    if index <= 0:
                        return instance_id, keypair, private_ip
                    index -= 1

        return instance_id, keypair, private_ip

    def _is_retryable_exception(exception):
        return not isinstance(exception, botocore.exceptions.ClientError)

    @retry(retry_on_exception=_is_retryable_exception, stop_max_delay=10000, wait_exponential_multiplier=500, wait_exponential_max=2000)
    def _ec2_describe_instances(self, **kwargs):
        return self.ec2.describe_instances(**kwargs)
