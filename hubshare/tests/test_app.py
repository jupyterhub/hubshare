import sys
from subprocess import check_output

def sh(*args, **kwargs):
    return check_output(*args, **kwargs).decode('utf8', 'replace')

def test_help():
    out = sh([sys.executable, '-m', 'hubshare', '-h'])

def test_version():
    out = sh([sys.executable, '-m', 'hubshare', '--version'])
    import pkg_resources
    expected = pkg_resources.get_distribution('hubshare').version
    assert out.strip() == expected
