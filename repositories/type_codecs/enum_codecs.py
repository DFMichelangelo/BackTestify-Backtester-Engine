from bson.codec_options import TypeCodec


class Enum_codec(TypeCodec):
    python_type = None    # the Python type acted upon by this type codec
    bson_type = str   # the BSON type acted upon by this type codec

    def __init__(self, python_type):
        self.python_type = python_type

    def transform_python(self, value):
        """Function that transforms a custom type value into a type
        that BSON can encode."""
        return value.value

    def transform_bson(self, value):
        """Function that transforms a vanilla BSON type value into our
        custom type."""
        return self.python_type(value) if value in self.python_type.__members__ else value
