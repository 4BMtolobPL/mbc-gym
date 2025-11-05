def test_sample():
    assert 1 == 1


def test_sample_fixture(app_data):
    assert app_data == 3
