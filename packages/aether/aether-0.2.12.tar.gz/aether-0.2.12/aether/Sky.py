
"""The Sky object provides user-developers with an interface to the Aether Platform
and larger functionality of cloud applications. Nearly every action taken by Aether
user-developers is built or executed by a method on the Sky object either through
direct method call or using the Sky object to pass-through a cloud operation to 
the Aether Platform ecosystem of applications and users.

The Aether Client provides a wrapper to most of the REST microservice calls that form
the foundation of the Aether ecosystem. The typical inheritance motif of the Sky object
is to receive an operating client in its constructor, then to use standard methods on the
Sky object to manage call methods on the client.

The Sky object provides the interface to the general application operating system of the
Aether Platform. In addition to this, methods are provided to give more conventional access
to high use operations like searching, cropping, and downloading through familiar direct
access to these applications using the Sky object.

In addition to this, methods are provided on the Sky object to:

1) :py:class:`~services.UserAdminServices`: manage the user and user account,
2) :py:class:`~services.AppSupportServices`: publish and interact with published applications,

For more information on these services see their respective classes.
"""

import json

import aetheruserconfig as cfg
from aether.proto import api_pb2
from aether.services.AppSupportServices import AppSupportServices
from aether.services.UserAdminServices import UserAdminServices
from aether.session.GlobalConfig import GlobalConfig
from aether.sky_utils import sky_utils
from base.GeoTiffResource import GeoTiffResource
from session.Exceptions import SkyValueError

class Sky(UserAdminServices, AppSupportServices):

    def __init__(self, aether_client):
        self._aether_client = aether_client

    def Resource(self, resource_name):
        """Access a Resource on the data platform, usually for search.

        Resources are data on the platform (e.g., GeoTiff data layer) against which
        algorithms, analytics, and meta-algorithms can be run.

        Args:
            resource_name (string): The name of the resource to search.

        Returns:
            response (:py:class:`~base.GeoTiffResource.GeoTiffResource`).
        """
        if resource_name not in cfg.resources:
            raise SkyValueError("Resource {} not found. Available resources: {}".format(resource_name, cfg.resources.keys()))

        return GeoTiffResource(self, resource_name, cfg.resources[resource_name])

    def search(self, resource_name, polygon, query_parameters, app=None):
        """Search a Resource for inclusion of a polygon matching query parameters.

        Args:
            resource_name (string): The name of the resource to search.

            polygon (:py:class:`~dataobjects.AEPolygon.AEPolygon`): The polygon, representing the lat-lng coordinates of the region of interest.

            query_parameters (dict): Key-value pairs of parameter name and value.
                See :py:class:`~base.QueryParameters.QueryParameters` for more information.

            app (:py:class:`~base.AppSupport.AppSupport`): Either an AppSupport object or None. Using
                AppSupport will compile the microservice into a deferred application
                for use; otherwise, passing None will execute the microservice
                at runtime.

        Returns:
            response (:py:class:`~base.SpacetimeBuilder.SpacetimeBuilder`): a SpacetimeBuilder if successful, and None
             if not. Returns a PlaceholderSpacetimeBuilder if app is not None.

            The SpacetimeBuilder contains a set of instructions to run another
            as a request to another application.

            The PlaceholderSpacetimeBuilder is returned when app is an AppSupport
            object. Its methods are equivalent to SpacetimeBuilder (so that code that
            follows will compile), but does not include the results of having run the
            application. Instead, the PlaceholderSpacetimeBuilder contains instructions
            to be substituted at runtime by the SpacetimeBuilder of the actual
            microservice output.
        """
        if resource_name not in cfg.resources:
            raise SkyValueError("ERROR: Resource {} not found. Available resources: {}".format(resource_name, cfg.resources.keys()))

        is_valid, msg = sky_utils.is_valid_search_parameters(resource_name, query_parameters)
        if not is_valid:
            raise SkyValueError(msg)

        # Confirm that all bands contain the same resolution imagery. Otherwise, crop will fail.
        if resource_name in cfg.reference and "bands" in query_parameters:
            resolutions = [cfg.reference[resource_name][b]["spatial_resolution_m"] for b in query_parameters["bands"]]
            if len(set(resolutions)) != 1:
                msg = "Query contains bands of different spatial resolution.\n"
                msg += "This will be supported soon. Until then please search, crop, and download grouped separatedly by resolution.\n"
                msg += "\n".join(["{}: {}m".format(b, cfg.reference[resource_name][b]["spatial_resolution_m"]) for b in query_parameters["bands"]])
                raise SkyValueError(msg)

        query_parameters.update(dict(polygon=polygon.to_latlngs()))
        output_structure = api_pb2.SpacetimeBuilder()
        response = self._aether_client.post_to("SearchResource",
                                               dict(resource_name=resource_name),
                                               query_parameters,
                                               output_structure=output_structure,
                                               app=app)
        return response

    def crop(self, builder, projection="epsg:3857", app=None):
        """Apply the crop application to a time series of imagery and polygon represented as a SpacetimeBuilder.

        Args:
            builder (:py:class:`~base.SpacetimeBuilder.SpacetimeBuilder`): The SpacetimeBuilder request contains a time series, each of which consists
             of a list of stubs which are concatenated as bands, then cropped to match the layout of the polygon.

            app (:py:class:`~base.AppSupport.AppSupport`): Either an AppSupport object or None. Using AppSupport will
             compile the microservice into a deferred application for use; otherwise, passing None will execute the
             microservice at runtime.

        Returns:
            response (:py:class:`~base.SpacetimeBuilder.SpacetimeBuilder`) A SpacetimeBuilder if successful, and None
             if not. Returns a PlaceholderSpacetimeBuilder if app is not None.

        The :py:class:`~base.SpacetimeBuilder.SpacetimeBuilder` contains a time series of stubs, each of which is a
        cropped GeoTiff created by the application. A mask (.msk) file is generated, if applicable, and a color table
        is appended for each stub which also has a color table added.
        """
        if projection is not None:
            projection = dict(init=projection)
            if not sky_utils.is_valid_projection(projection):
                raise SkyValueError("ERROR: Requested projection '{}' is not valid.".format(projection))

        output_structure = api_pb2.SpacetimeBuilder()
        uri_parameters = dict(builder=sky_utils.serialize_pb(builder), projection=json.dumps(projection))
        # input_structure = ["builder"]
        response = self._aether_client.post_to("ClipAndShipResource",
                                               {},
                                               uri_parameters,
                                               # input_structure=input_structure,
                                               output_structure=output_structure,
                                               app=app)

        return response

    def download(self, builder, run=None, app=None):
        """Downloads the contents of a :py:class:`~base.SpacetimeBuilder.SpacetimeBuilder`, i.e., a time series of imagery masked to a polygon.

        Args:
            builder (:py:class:`~base.SpacetimeBuilder.SpacetimeBuilder`): The SpacetimeBuilder request contains a time series, each of which consists
             of a list of stubs which are concatenated as bands, stacked into a time series, and downloaded.

            run (list): A list of any functions which accepts a Spacetime object (not protobuffer) as input
                and products a Spacetime object as output can be sent along with the SpacetimeBuilder to be run prior to
                download. This allows a convenient and lightweight mechanism for running simple algorithms in the cloud.
                The functions are limited to native python and numpy operations, if the method imports numpy.

            app (:py:class:`~base.AppSupport.AppSupport`): Either an AppSupport object or None. Using AppSupport will
                compile the microservice into a deferred application for use; otherwise, passing None will execute the
                microservice at runtime.

        Returns:
            response (Spacetime): a Spacetime protocol buffer if successful, and None if not. Returns a PlaceholderSpacetime if app
                is not None.

            The Spacetime contains a time series of imagery, each of which is a cropped and masked to the dimensions of
            the originating polygon. The metadata for the originating earliest timestamp GeoTiff is included as well.
        """
        if run is not None:
            byte_ops = [sky_utils.serialize_to_bytestring(r) for r in run]
            for op in byte_ops:
                bop = builder.btops.add()
                bop.serialized_func = op

        uri_parameters = dict(builder=sky_utils.serialize_pb(builder),
                              method="DownloadSpacetime",
                              )
        output_structure = api_pb2.Spacetime()
        response = self._aether_client.post_to("GatewaySpacetimeBuilder",
                                               {},
                                               uri_parameters,
                                               # input_structure=input_structure,
                                               output_structure=output_structure,
                                               app=app)
        return response



    def RunApplicationWithPayload(self, payload, polygon):
        """Runs a compiled applications from using its payload string.

        Args:
            payload (str): The product of :py:class:`~Sky.Sky` :py:meth:`~dataobjects.AppSupportServices.AppSupportServices.ApplicationPayload` method.
            polygon (:py:class:`~dataobjects.AEPolygon.AEPolygon`): The polygon, representing the lat-lng coordinates of the region of interest.

        Returns:
            response (:py:class:`HttpResponse`): a dictionary containing the application results, usually a serialized
                string containing an image.
        """
        uri_parameters = dict(polygon=polygon.to_latlngs(),
                              payload=payload)

        response = self._aether_client.post_to("SkyApplicationManifest",
                                               {},
                                               uri_parameters)

        return response

    def RunApplicationWithId(self, application_id, polygon, as_uuid=None):
        """Runs a compiled applications from using its Application Id string.

        Args:
            application_id (str): The application id of the saved application after calling the
                :py:class:`~Sky.Sky` :py:meth:`~dataobjects.AppSupportServices.AppSupportServices.PublishApplication` method.
            polygon (:py:class:`~dataobjects.AEPolygon.AEPolygon`): The polygon, representing the lat-lng coordinates of the region of interest.

        Returns:
            response (:obj:`HttpResponse`): a dictionary containing the application results, usually a serialized
             string containing an image.
        """
        if as_uuid is None:
            as_uuid = GlobalConfig._getInstance().uuid
        uri_parameters = dict(polygon=str(polygon.to_latlngs()))
        response = self._aether_client.post_to("EndpointConsumerInterface",
                                               dict(uuid=as_uuid, application_id=application_id),
                                               uri_parameters)
        return response
