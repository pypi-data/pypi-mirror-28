import base64

import numpy as np
from PIL import Image

from aether.proto.api_pb2 import Spacetime as Spacetime_pb
from aether.sky_utils import sky_utils


class Spacetime(object):

    def __init__(self, stack, timestamps, metadata):
        self._stack = stack if len(stack.shape) == 4 else np.expand_dims(stack, axis=3)
        self._timestamps = timestamps
        self._metadata = metadata

    def update(self, stack, timestamps, metadata):
        self._stack = stack if len(stack.shape) == 4 else np.expand_dims(stack, axis=3)
        self._timestamps = timestamps
        self._metadata = metadata
        return self

    def timestamps(self):
        return self._timestamps

    def metadata(self):
        return self._metadata

    def as_numpy(self):
        return self._stack

    def band(self, b):
        return self._stack[:,:,:,b]

    def generate_image(self, ts, bands, show_now=True, save_to=None):
        if isinstance(ts, str):
            if ts not in self._timestamps:
                print("Timestamp {} not found in Spacetime with timestamps {}".format(ts, self._timestamps))
                return
            ts = self._timestamps.index(ts)
        for b in bands:
            if b > self._stack.shape[3] - 1:
                print("Band Index {} out of range.".format(b))
                return

        # Normalizes to 0 to 1.
        d = self._stack[ts][:,:,bands] # This seems to be a weird new change of functionality.
        v_min, v_max = np.nanmin(d), np.nanmax(d)
        r = 1.0 if v_max == v_min else v_max - v_min
        d -= v_min
        d *= 255.0 / r

        mode = "RGB" if len(bands) == 3 else "L"
        d = d if len(bands) == 3 else d[:,:,0]
        image = Image.fromarray(np.array(d, dtype=np.uint8), mode=mode)
        if show_now:
            image.show()
        if save_to is not None:
            image.save(save_to)


    def generate_chart(self, bands, show_now=True, save_to=None, subsample_to=None):
        pass

    @staticmethod
    def from_pb(s, app=None):
        if app is not None:
            return s.from_pb(s)

        shape = np.array(s.array_shape)
        stack = np.frombuffer(sky_utils.deserialize_numpy(s.array_values), dtype=np.float)
        stack = np.reshape(stack, newshape=shape)
        timestamps = s.timestamps
        metadata = s.metadata
        return Spacetime(stack, timestamps, metadata)

    def to_pb(self):
        s = Spacetime_pb()
        s.timestamps.extend(self.timestamps())
        s.metadata = str(self._metadata)
        s.array_shape.extend(list(self.as_numpy().shape))
        s.array_values = base64.b64encode(self.as_numpy())
        return s