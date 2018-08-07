from globalgiving_utilities import Organization
import re

def parse_record(entry):
    fields = entry.split(',')
    if fields[0] == "" or fields[0] == "id":
        return

    new_organization = Organization()
    new_organization.id = "o.example.{}".format(fields[0])
    new_organization.name = ' '.join([i.capitalize() for i in fields[1].split(' ')])
    new_organization.add_registration("US", fields[0])
    new_organization.ids["example"] = fields[0]
    if fields[2]:
        website = fields[2]
        if not bool(re.match('http', website, re.I)):
            website = "http://" + website
        new_organization.website = website
    address = {
        "address_1": fields[3] or None,
        "city": fields[4] or None,
        "state": fields[5] or None,
        "postal": fields[6] or None,
        "country": "United States"
    }
    new_organization.mailing_address = {key: value for key, value in address.items() if value}
    print(new_organization.to_dict())

def parse_file(filename):
    with open(filename) as data_file:
        for entry in data_file:
            entry = entry.rstrip()
            parse_record(entry)

def main():
    parse_file("example_data.csv")

if __name__ == '__main__':
    main()