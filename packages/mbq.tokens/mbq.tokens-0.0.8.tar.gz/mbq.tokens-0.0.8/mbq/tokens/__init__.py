from .decoder import Decoder
from .exceptions import TokenError  # noqa


def init(certificate=None, allowed_audiences=None):
    decoder = Decoder(
        certificate=certificate,
        allowed_audiences=allowed_audiences,
    )

    global decode, decode_header, decode_with_unknown_audience
    decode = decoder.decode
    decode_header = decoder.decode_header
    decode_with_unknown_audience = decoder.decode_with_unknown_audience
