import responses
from flask import Flask

from archivy import data
from archivy.extensions import get_db


def test_parse_pocket(test_app, client, mocked_responses, pocket_fixture):
    """Test the /pocket endpoint

    HTTP calls to the pocket API are mocked out
    """

    # fake website
    mocked_responses.add(responses.GET, "https://example.com/", body="""<html>
        <head><title>Example</title></head><body><p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit
        </p></body></html>
    """)



    r: Flask.response_class = client.get('/parse_pocket?new=1')
    assert r.status_code == 302

    dataobjs = data.get_items()
    assert len(dataobjs.child_files) == 1


def test_pocket_with_empty_title(test_app, client, pocket_fixture,
                                 mocked_responses):
    """Test the /pocket endpoint

    HTTP calls to the pocket API are mocked out
    """

    # fake website
    mocked_responses.add(responses.GET, "https://example.com/", body="""<html>
        <head></head><body><p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit
        </p></body></html>
    """)

    r: Flask.response_class = client.get('/parse_pocket?new=1')
    assert r.status_code == 302

    dataobjs = data.get_items()
    assert len(dataobjs.child_files) == 1


