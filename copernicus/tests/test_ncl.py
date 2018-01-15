from subprocess import check_output


def test_ncl_version():
    assert '6.4.0' in check_output(["ncl", "-V"])
