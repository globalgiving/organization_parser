from .organization import Organization
import pytest

def test_is_valid_bad():
    org = Organization()
    assert not org.is_valid()

def test_is_valid_good():
    org = Organization()
    org.name = "Test"
    org.id = "o.test.1234"
    org._registration_id = "1324"
    org._registration_country = "US"
    org.source = "test"
    assert org.is_valid()

def test_add_registration():
    org = Organization()
    org.add_registration("US", "1234")
    assert org._registration_country == "US"
    assert org._registration_id == "1234"
    assert org._registrations == [{"country":"US", "id":"1234"}]
    org.add_registration("GB", "4321")
    assert org._registration_country == "US"
    assert org._registration_id == "1234"
    assert org._registrations == [{"country":"US", "id":"1234"},{"country":"GB", "id":"4321"}]


def test_add_alternative():
    org = Organization()
    org.name = "Clean Water"
    org.source = "testsource"
    org.language = "en"
    org.add_alternative("name", "Googly moogly", "test2", "xx")
    assert org._alternatives == {
        "name": {
            "test2": {
                "language": "xx",
                "value": "Googly moogly"
            }
        }
    }

def test_add_alternative_two():
    org = Organization()
    org.name = "Clean Water"
    org.source = "testsource"
    org.language = "en"
    org.add_alternative("name", "Googly moogly", "test2", "xx")
    org.add_alternative("name", "Mongo Bongo", "test3", "qr")
    assert org._alternatives == {
        "name": {
            "test2": {
                "language": "xx",
                "value": "Googly moogly"
            },
            "test3": {
                "language": "qr",
                "value": "Mongo Bongo"
            }
        }
    }

def test_add_alternative_default():
    org = Organization()
    org.name = "Clean Water"
    org.source = "testsource"
    org.language = "es"
    org.add_alternative("name", "Googly moogly", "test2")
    assert org._alternatives == {
        "name": {
            "test2": {
                "language": "en",
                "value": "Googly moogly"
            }
        }
    }


def test_to_dict():
    org = Organization()
    org.name = "Test"
    org.id = "o.test.1234"
    org._registration_id = "1234"
    org._registration_country = "US"
    org._registrations.append({"country":"US", "id":"1234"})
    org.external_field["something"] = "foo"
    org.year_founded = "1999"
    assert org.to_dict() == {
        "id": "o.test.1234",
        "registration_country": "US",
        "registation_id": "1234",
        "registrations": [{"country":"US", "id":"1234"}],
        "name": "Test",
        "something": "foo",
        "year_founded": 1999,
        "language": "en"
    }