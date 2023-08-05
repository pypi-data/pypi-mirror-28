import dill
import base64
from google.protobuf import json_format
import aetheruserconfig as cfg
import pyproj
import io
from PIL import Image

class sky_utils(object):

    @staticmethod
    def serialize_to_bytestring(o):
        b = bytearray()
        b.extend(dill.dumps(o, protocol=2))
        return str(b)

    @staticmethod
    def deserialize_from_bytestring(s):
        return dill.loads(bytes(s))

    @staticmethod
    def serialize_for_url(o):
        return base64.urlsafe_b64encode(str(o))

    @staticmethod
    def deserialize_from_url(s):
        return base64.urlsafe_b64decode(str(s))

    @staticmethod
    def serialize_numpy(n):
        return base64.b64encode(n)

    @staticmethod
    def deserialize_numpy(s):
        return base64.b64decode(s)

    @staticmethod
    def serialize_pb(pb):
        return json_format.MessageToJson(pb)

    @staticmethod
    def deserialize_pb(s, pb):
        return json_format.Parse(s, pb)

    @staticmethod
    def generate_image_from_http_response(image_data):
        return Image.open(io.BytesIO(sky_utils.deserialize_from_url(image_data)))

    @staticmethod
    def is_valid_search_parameters(resource_name, query_parameters):
        allowed_query_parameters = {q.name:q for q in cfg.resources[resource_name]["_query_parameters"]}
        for p in allowed_query_parameters.values():
            if p.is_required and p.name not in query_parameters:
                return False, "Search query is missing parameter '{}'.".format(p.name)

        for name in query_parameters.keys():
            if name not in allowed_query_parameters.keys():
                return False, "Unrecognized query parameter '{}'.".format(name)

            if not allowed_query_parameters[name].is_valid_value(query_parameters[name]):
                return False, "Query parameter '{}' value is not value: {}.".format(name, query_parameters[name])
        return True, None

    @staticmethod
    def is_valid_projection(projection):
        try:
            pyproj.Proj(projection)
            return True
        except:
            return False
