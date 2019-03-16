import pytest

@pytest.mark.parametrize('endpoint', [
    "images/",
    "texts/",
    "scraping-tasks/"
])
def test_get_empty_collections(client, endpoint):
    r = client.get('/api/' + endpoint)
    assert r.status_code == 200
    assert r.get_json() == []


@pytest.mark.parametrize('endpoint, resource_name',[
    ('images/222/', 'Image'),
    ('images/1311/content', 'Image'),
    ('texts/12/', 'Text'),
    ('texts/1111/content', 'Text'),
    ('scraping-tasks/2333', 'Task')
])
def test_get_non_existing_resource(client, endpoint, resource_name):
    r = client.get('/api/' + endpoint)
    #assert r.status_code == 404
    assert str(r.data, encoding='utf-8') == "{} with given id does not exist".format(resource_name)

