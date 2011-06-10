


def test_compile():
    try:
        import tiddlywebplugins.atombag
        assert True
    except ImportError, exc:
        assert False, exc
