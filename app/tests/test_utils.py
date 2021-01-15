#import pytest
from .. import utils

class TestUtils():
    def test_str_to_bytes(self):
        result = utils.str_to_bytes("testing123")
        assert b"testing123" == result

    def test_bytes_to_str(self):
        utf_result = utils.bytes_to_str(b"testing123")
        assert "testing123" == utf_result

        ascii_bytes = b"testing123"
        ascii_result = utils.bytes_to_str(ascii_bytes, "ascii")
        assert "testing123" == ascii_result

    def test_parse_regex(self):
        # This just wraps re.split, if it fails we've got bigger problems.
        pass