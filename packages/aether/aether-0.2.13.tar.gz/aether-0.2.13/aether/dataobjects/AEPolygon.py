import json
from aether.datamodel.ae_DataObject import ae_DataObject

class AEPolygon(object):
    """An object to make latlng/lnglat polygons easier. All platform operations are written to use AEPolygon objects, so
    as to not confuse latitude/longitude order using third-party systems with varying conventions.

    To quote from Stack Overflow:

    EPSG:4326 specifically states that the coordinate order should be latitude, longitude. Many software packages still
    use longitude, latitude ordering. This situation has wreaked unimaginable havoc on project deadlines and programmer
    sanity.
    """

    _object_type_name = "AEPolygon"

    def __init__(self):
        self._lats, self._lngs = [], []
        # super(AEPolygon, self).__init__(self._object_type_name)

    def __repr__(self):
        return "AEPolygon()"

    def __str__(self):
        return "AEPolygon(lats={}, lngs={})".format(self.lats(), self.lngs())

    def lats(self):
        """Returns the coordinate latitude values as an array."""
        return self._lats

    def lngs(self):
        """Returns the coordinate longitude values as an array."""
        return self._lngs

    def latlngs(self):
        """Returns the coordinate latitude-longitude values as an Nx2 array."""
        return map(list, zip(*[self.lats(), self.lngs()]))

    def lnglats(self):
        """Returns the coordinate longitude-latitude values as an Nx2 array."""
        return map(list, zip(*[self.lngs(), self.lats()]))

    def from_lats_and_lngs(self, lats, lngs):
        """Loads a polygon using coordinate longitude and latitude values."""
        if self._is_string(lats):
            lats = self._str_to_arr(lats)
        if self._is_string(lngs):
            lngs = self._str_to_arr(lngs)
        self._lats = lats
        self._lngs = lngs
        return self

    def from_latlngs(self, latlngs):
        """Loads a polygon using coordinate longitude and latitude values."""
        if self._is_string(latlngs):
            latlngs = self._str_to_arr(latlngs)
        s = map(list, zip(*latlngs))
        self._lats = s[0]
        self._lngs = s[1]
        return self

    def from_lnglats(self, lnglats):
        """Loads a polygon using coordinate longitude and latitude values."""
        if self._is_string(lnglats):
            lnglats = self._str_to_arr(lnglats)
        s = map(list, zip(*lnglats))
        self._lats = s[1]
        self._lngs = s[0]
        return self

    # A tuple ordered (left, bottom, right, top)
    def from_bounds(self, bounds):
        """Loads a polygon using coordinate boundaries as a 4-tuple: (western longitude, southern latitude, eastern longitude, northern latitude)."""
        self._lats = [bounds[1], bounds[1], bounds[3], bounds[3], bounds[1]]
        self._lngs = [bounds[0], bounds[2], bounds[2], bounds[0], bounds[0]]
        return self

    # A tuple ordered (left, bottom, right, top)
    def to_bounds(self):
        """Returns a polygon coordinate boundaries as a 4-tuple: (western longitude, southern latitude, eastern longitude, northern latitude)."""
        return [min(self._lngs), min(self._lats), max(self._lngs), max(self._lats)]

    def to_latlngs(self):
        return map(list, zip(*[self._lats, self._lngs]))

    def to_lnglats(self):
        return map(list, zip(*[self._lngs, self._lats]))

    def to_latlng_bounds(self):
        bounds_dict = dict(
            north_lat=max(self._lats),
            south_lat=min(self._lats),
            east_lon=max(self._lngs),
            west_lon=min(self._lngs),
        )
        return bounds_dict

    @staticmethod
    def _is_string(s):
        return isinstance(s, str) or isinstance(s, unicode)

    @staticmethod
    def _str_to_arr(s):
        return json.loads(s)

    def _to_dm_dict(self):
        dm = dict(
            lats=self.lats(),
            lngs=self.lngs()
        )
        return dm

    def _from_dm_dict(self, dm):
        return self.from_lats_and_lngs(dm["lats"], dm["lngs"])
