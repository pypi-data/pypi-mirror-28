################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

import json
from .wml_client_error import MissingValue, WMLClientError, NoWMLCredentialsProvided, ApiRequestFailure, UnexpectedType
from .href_definitions import HrefDefinitions
from .log_util import get_logger


class WMLResource:
    def __init__(self, name, client, wml_credentials, wml_token, instance_details):
        self.logger = get_logger(name)
        if client is None:
            raise MissingValue('client')
        if wml_credentials is None:
            raise NoWMLCredentialsProvided
        if wml_token is None:
            raise MissingValue('wml_token')
        if instance_details is None:
            raise MissingValue('instance_details')
        self._client = client
        self._wml_credentials = wml_credentials
        self._wml_token = wml_token
        self._instance_details = instance_details
        self._href_definitions = HrefDefinitions(wml_credentials)

    def _handle_response(self, expected_status_code, operationName, response, json_response=True):
        if response.status_code == expected_status_code:
            self.logger.info('Successfully finished {} for url: \'{}\''.format(operationName, response.url))
            self.logger.debug('Response({} {}): {}'.format(response.request.method, response.url, response.text))
            if json_response:
                try:
                    return json.loads(response.text)
                except Exception as e:
                    raise WMLClientError('Failure during parsing json response: \'{}\''.format(response.text), e)
            else:
                return response.text
        else:
            raise ApiRequestFailure('Failure during {}.'.format(operationName), response)

    @staticmethod
    def _get_required_element_from_dict(el, root_path, path):
        WMLResource._validate_type(el, root_path, dict)
        WMLResource._validate_type(root_path, 'root_path', str)
        WMLResource._validate_type(path, 'path', list)

        if path.__len__() < 1:
            raise WMLClientError('Unexpected path length: {}'.format(path.__len__))

        try:
            new_el = el[path[0]]
            new_path = path[1:]
        except Exception as e:
            raise MissingValue(root_path + '.' + str(path[0]), e)

        if path.__len__() > 1:
            return WMLResource._get_required_element_from_dict(new_el, root_path + '.' + path[0], new_path)
        else:
            if new_el is None:
                raise MissingValue(root_path + '.' + str(path[0]))

            return new_el

    @staticmethod
    def _validate_type(el, el_name, expected_type, mandatory=True):
        if el_name is None:
            raise MissingValue('el_name')

        if type(el_name) is not str:
            raise UnexpectedType('el_name', str, type(el_name))

        if expected_type is None:
            raise MissingValue('expected_type')

        if type(expected_type) is not type:
            raise UnexpectedType('expected_type', type, type(expected_type))

        if type(mandatory) is not bool:
            raise UnexpectedType('mandatory', bool, type(mandatory))

        if mandatory and el is None:
            raise MissingValue(el_name)
        elif el is None:
            return

        if not isinstance(el, expected_type):
            raise UnexpectedType(el_name, expected_type, type(el))
