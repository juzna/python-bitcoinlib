import asn1


def parse_sig(buf):
    """Parse a signature in DER format into (r, s, hash_type).

    Args:
        buf: bytes buffer

    Returns: (r, s, hashtype); all integers
    """
    d = asn1.Decoder()
    d.start(buf[0:-1])  # last byte is hashtype
    d.enter()
    _, r = d.read()
    _, s = d.read()
    return r, s, buf[-1]
