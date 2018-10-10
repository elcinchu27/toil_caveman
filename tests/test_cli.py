"""toil_caveman cli tests."""

from os.path import join

import pytest

from toil_caveman import cli


def test_main():
    """Sample test for main command."""
    with pytest.raises(SystemExit) as _:
        cli.main()
