import boto3
import botocore.session
import logging
from logging import NullHandler
from boto3_extensions.arn_patch import patch_session, \
                                   patch_service_context, \
                                   patch_resource_factory, \
                                   patch_resource_meta, \
                                   patch_create_request_parameters
from os import environ, path
from imp import reload

logging.getLogger(__name__).addHandler(NullHandler())
_logger = logging.getLogger(__name__)

dir_path = path.dirname(path.realpath(__file__))
environ['AWS_DATA_PATH'] = '{dir_path}/data/'.format(dir_path=dir_path)
reload(boto3)


def arn_patch_boto3():
    """
    Patch boto3 to support ARNs for all resources
    """
    patch_session()
    patch_service_context()
    patch_resource_factory()
    patch_resource_meta()
    patch_create_request_parameters()
    _logger.info('Patched Boto3 with arn support')


def get_role_session(role_arn,
                     role_session_name=None,
                     base_session=None,
                     **kwargs):

    botocore_session = botocore.session.Session()
    botocore_session.full_config['profiles'][role_arn] = {
        'role_arn': role_arn,
        'credential_source': 'Ec2InstanceMetadata',
        'session_name': role_session_name
    }

    session = boto3.Session(
        profile_name=role_arn, botocore_session=botocore_session, **kwargs)

    if base_session:

        def client_creator(*args, **kwargs):
            return base_session.create_client('sts')

        session._session.get_component('credential_provider').get_provider(
            'assume-role')._client_creator = client_creator

    return session


class ConnectionManager:
    '''
    Usage:
        connections = ConnectionManager(region_name='us-east-1')
        session = connections.get_session(role_arn='arn:aws:iam::1234567890:role/test-role', role_session_name='test')

    You can also provide a base session if you prefer:
        connections = ConnectionManager(session=my_boto3_session)

    '''

    def __init__(self, session=None, **kwargs):
        self._base_session = session
        self.default_session_args = kwargs
        self.connections = {}

    def get_session(self, role_arn, role_session_name):

        if (role_arn, role_session_name) not in self.connections:
            session = get_role_session(role_arn, role_session_name,
                                       self._base_session,
                                       **self.default_session_args)
            self.connections[(role_arn, role_session_name)] = session
        return self.connections[(role_arn, role_session_name)]
