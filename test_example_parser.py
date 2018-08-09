import pytest
import random
import string

import example_parser
from globalgiving_utilities import Organization

@pytest.fixture()
def temp_file(tmpdir):
    """Generates a random tempfile name to use for testing file access."""
    return str(tmpdir.join(''.join(random.choices(string.ascii_uppercase + string.digits, k=8))))

called = False
def test_main(monkeypatch):
    global called
    called = False

    def mock_parse_file(filename):
        global called
        called = True
        assert filename

    monkeypatch.setattr(example_parser, "parse_file", mock_parse_file)
    example_parser.main()
    assert called, "parse_file was never called"

def test_parse_file(monkeypatch, temp_file):
    global called
    called = 0
    
    with open(temp_file, 'w')as temp_write:
        temp_write.write('id,name,something\n')
        temp_write.write('123,a,b\n')
        temp_write.write('345,c,d\n')

    def mock_parse_record(entry):
        global called
        called += 1

    monkeypatch.setattr(example_parser, "parse_record", mock_parse_record)
    example_parser.parse_file(temp_file)
    assert called == 3, "parse_record called incorrect number of times"

temp_org = None
test_cases = [
    pytest.param(
        "576,SHAVE THE WHALES,shavethewhales.org,123 Fake Street,Nowhere,AL,00321",
        {'id': 'o.example.576', '_registration_country': 'US', '_registration_id': '576', '_registrations': [{'country': 'US', 'id': '576'}], 'ids': {'example': '576'}, 'name': 'Shave The Whales', 'website': 'http://shavethewhales.org', 'mailing_address': {'address_1': '123 Fake Street', 'city': 'Nowhere', 'state': 'AL', 'postal': '00321', 'country': 'United States'}, 'phone': None, 'year_founded': None, 'inactive': False, 'external_field': {}},
        id="576"
    ),
    pytest.param(
        "982,Save the bunnies,,,,,",
        {'id': 'o.example.982', '_registration_country': 'US', '_registration_id': '982', '_registrations': [{'country': 'US', 'id': '982'}], 'ids': {'example': '982'}, 'name': 'Save The Bunnies', 'website': None, 'mailing_address': {'country': 'United States'}, 'phone': None, 'year_founded': None, 'inactive': False, 'external_field': {}},
        id="982"
    ),
    pytest.param(
        "1230,Water My Flowrs,https://www.flowers.org/,431 Flower Way,Petaltown,FL,33435",
        {'id': 'o.example.1230', '_registration_country': 'US', '_registration_id': '1230', '_registrations': [{'country': 'US', 'id': '1230'}], 'ids': {'example': '1230'}, 'name': 'Water My Flowrs', 'website': 'https://www.flowers.org/', 'mailing_address': {'address_1': '431 Flower Way', 'city': 'Petaltown', 'state': 'FL', 'postal': '33435', 'country': 'United States'}, 'phone': None, 'year_founded': None, 'inactive': False, 'external_field': {}},
        id="1230"
    ),
    pytest.param(
        "id,name,website,address,city,state,zip",
        None,
        id="title_row"
    )
]

@pytest.mark.parametrize("entry,output",test_cases)
def test_parse_record(monkeypatch,entry,output):
    global called
    global temp_org
    called = [False,False]
    temp_org = None

    class MockOrganization(Organization):
        def __init__(self):
            global called
            global temp_org
            called[0] = True
            temp_org = self
            super(MockOrganization, self).__init__()
        def upload(self):
            global called
            called[1] = True

    monkeypatch.setattr(example_parser, "Organization", MockOrganization)
    example_parser.parse_record(entry)
    if output:
        assert called[0]
        assert called[1]
        assert temp_org.id == output['id']
        assert temp_org.__dict__ == output
    else:
        assert not called[0]
        assert not called[1]
