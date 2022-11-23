import sys
from unittest.mock import Mock, call

from parble.utils import Spinner


def test_spin():
    stream = Mock(spec=sys.stdout)

    with Spinner(stream=stream):
        pass

    assert stream.write.call_count == 4
    stream.write.assert_has_calls([call("-"), call("\b"), call(" "), call("\b")])
    assert stream.flush.call_count == 2


def test_spin_disabled():
    stream = Mock(spec=sys.stdout)

    with Spinner(disabled=True, stream=stream):
        pass

    assert stream.write.call_count == 0
    assert stream.flush.call_count == 0


def test_spin_not_tty():
    stream = Mock(spec=sys.stdout)
    stream.isatty.return_value = False

    with Spinner(stream=stream):
        pass

    assert stream.write.call_count == 0
    assert stream.flush.call_count == 0


def test_spin_not_tty_force():
    stream = Mock(spec=sys.stdout)
    stream.isatty.return_value = False

    with Spinner(stream=stream, forced=True):
        pass

    assert stream.write.call_count == 4
    stream.write.assert_has_calls([call("-"), call("\b"), call(" "), call("\b")])
    assert stream.flush.call_count == 2
