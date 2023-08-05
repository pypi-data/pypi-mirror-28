from aether.app_io_utilities import app_io_utilities
import aether.aetheruserconfig as cfg
import json
import copy
import requests
from session.Exceptions import SkyRuntimeError

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class aether_client(object):

    def __init__(self, uuid, hostport, protocol):
        self._uuid = uuid
        self._hostport = hostport
        self._protocol = protocol

    def _make_call(self, request, hostport):
        logger.info("Making REST call to: {} with {}".format(hostport, request))
        try:
            url = "{protocol}{hostport}{entry}".format(protocol=self._protocol, hostport=hostport, entry=request["entry"])
            headers = {'Content-Transfer-Encoding': 'base64'}
            response = requests.request(request["method"], url, json=request["data"], headers=headers)
        except Exception, err:
            raise SkyRuntimeError(err)
        return response

    def _make_request(self, entry_name, entry_parameters, uri_parameters):
        if entry_name not in cfg._rest_entrypoints:
            raise SkyRuntimeError("Requested entrypoint unrecognized: {}".format(entry_name))

        request = copy.deepcopy(cfg._rest_entrypoints[entry_name])
        try:
            request["entry"] = request["entry"].format(**entry_parameters)
        except Exception:
            raise SkyRuntimeError("Requested entrypoint required parameters missing: {}".format(entry_name))

        request["data"] = uri_parameters
        return request

    def post_to(self, entry_name, entry_parameters, uri_parameters, output_structure=None, app=None):
        uri_parameters.update(dict(uuid=self._uuid))

        # if input_structure is not None:
        #     uri_parameters = self.serialize_to_input(uri_parameters, input_structure)
        #     if uri_parameters is None:
        #         logger.error("uri_parameters incorrectly formed by input_structure.")
        #         return None

        request = self._make_request(entry_name, entry_parameters, uri_parameters)

        if app is not None:
            return app.add(request, None, output_structure, "MICROSERVICE")
        return self.post_request(request, output_structure)

    def post_request(self, request, output_structure):
        response = self._make_call(request, self._hostport)

        if not response.ok:
            raise SkyRuntimeError("Request failed {}: {}".format(response.reason, response.content))

        try:
            content = json.loads(response.content)
        except Exception:
            raise SkyRuntimeError("Request returned ill formed JSON: {}".format(response.content))

        if output_structure is not None:
            return app_io_utilities.marshal_output(content, output_structure)
        return content
