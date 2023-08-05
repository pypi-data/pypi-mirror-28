""" AWS authentication """
#pylint: disable=C0325
import os
import base64
import xml.etree.ElementTree as ET
from collections import namedtuple
from ConfigParser import RawConfigParser
import boto3
from botocore.exceptions import ClientError

class AwsAuth(object):
    """ Methods to support AWS authentication using STS """

    def __init__(self, profile, verbose):
        home_dir = os.path.expanduser('~')
        self.creds_dir = home_dir + "/.aws"
        self.creds_file = self.creds_dir + "/credentials"
        self.profile = profile
        self.verbose = verbose

    @staticmethod
    def choose_aws_role(assertion):
        """ Choose AWS role from SAML assertion """
        aws_attribute_role = 'https://aws.amazon.com/SAML/Attributes/Role'
        attribute_value_urn = '{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue'
        roles = []
        role_tuple = namedtuple("RoleTuple", ["principal_arn", "role_arn"])
        root = ET.fromstring(base64.b64decode(assertion))
        for saml2attribute in root.iter('{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'):
            if saml2attribute.get('Name') == aws_attribute_role:
                for saml2attributevalue in saml2attribute.iter(attribute_value_urn):
                    roles.append(role_tuple(*saml2attributevalue.text.split(',')))

        for index, role in enumerate(roles):
            role_name = role.role_arn.split('/')[1]
            print("%d: %s" % (index+1, role_name))
        role_choice = input('Please select the AWS role: ')-1
        return roles[role_choice]

    @staticmethod
    def get_sts_token(role_arn, principal_arn, assertion):
        """ Gets a token from AWS STS """
        ## Connect to the GovCloud STS endpoint if a GovCloud ARN is found.
        arn_region = principal_arn.split(':')[1]
        if arn_region == 'aws-us-gov':
            sts = boto3.client('sts', region_name='us-gov-west-1')
        else:
            sts = boto3.client('sts')
        response = sts.assume_role_with_saml(RoleArn=role_arn,
                                             PrincipalArn=principal_arn,
                                             SAMLAssertion=assertion)
        credentials = response['Credentials']
        return credentials

    def check_sts_token(self, profile):
        """ Verifies that STS credentials are valid """
        # Don't check for creds if profile is blank
        if not profile:
            return False

        parser = RawConfigParser()
        parser.read(self.creds_file)

        if not os.path.exists(self.creds_dir):
            if self.verbose:
                print("AWS credentials path does not exit. Not checking.")
            return False

        elif not os.path.isfile(self.creds_file):
            if self.verbose:
                print("AWS credentials file does not exist. Not checking.")
            return False

        elif not parser.has_section(profile):
            if self.verbose:
                print("No existing credentials found. Requesting new credentials.")
            return False

        session = boto3.Session(profile_name=profile)
        sts = session.client('sts')
        try:
            sts.get_caller_identity()

        except ClientError as ex:
            if ex.response['Error']['Code'] == 'ExpiredToken':
                print("Temporary credentials have expired. Requesting new credentials.")
                return False

        if self.verbose:
            print("STS credentials are valid. Nothing to do.")
        return True

    def write_sts_token(self, profile, access_key_id, secret_access_key, session_token):
        """ Writes STS auth information to credentials file """
        region = 'us-east-1'
        output = 'json'
        if not os.path.exists(self.creds_dir):
            os.makedirs(self.creds_dir)
        config = RawConfigParser()

        if os.path.isfile(self.creds_file):
            config.read(self.creds_file)

        if not config.has_section(profile):
            config.add_section(profile)

        config.set(profile, 'output', output)
        config.set(profile, 'region', region)
        config.set(profile, 'aws_access_key_id', access_key_id)
        config.set(profile, 'aws_secret_access_key', secret_access_key)
        config.set(profile, 'aws_session_token', session_token)

        with open(self.creds_file, 'w+') as configfile:
            config.write(configfile)
        print("Temporary credentials written to profile: %s" % profile)
        print("Invoke using: aws --profile %s <service> <command>" % profile)
