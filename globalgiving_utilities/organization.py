"""Moonshot Organization Importer."""

from typing import Optional, Text, List, Dict

__version__ = '0.0.1'
__all__ = [
    'Organization'
]

class Organization(object):

    """A non-governmental/charity/non-profit organization.

    Tips:
        If the database this organization is sourced from is the US IRS, then
        things should look like this:

            id: o.irs.12345
            ids: {"irs": "12345"}
            add_registration("US", "12345")
        
        The same would hold true for other databases.  Pick a "short name" for
        the database the data is coming from, and use it as part of the ``id``
        and ``ids`` entries.
    
    Attributes:
        id: A string containing the id of the organization. Should be in the
            format of "o.[source].[govt_id]".  Examples:

            o.irs.2342342
            o.gg.2132

        ids: All known external database IDs.  This should include the database
            this record came from.  An org sourced from the IRS would have an entry
            with key "irs" and value containing the EIN (the IRS's id number for
            the org) of the org.
        name: The name of this organization.  We would prefer this be in "Title Case".
        website: The full URL of the organization's website if it is known.
            Example: https://www.something.org/
        mailing_address: Address details of where the organization is
            physically located.  The following is a list of our standard field
            names for this dict:

            address_1
            address_2
            state
            city
            county
            country - This should be the full country name.
            postal
            neighborhood
            sublocality
            housenumber
            postal_town
            subpremise
            postal_code_suffix

            Use as many or as few of these as you need.
            
            Remember: Even if you don't have the address, you likely know what
            country they are in.
        phone: A string containing the phone number.  String out any formatting
            characters (hyphen, period, parenthesis, etc.)
        year_founded: A number that is the year the org was originally founded.
        inactive: False if the org is still operating, otherwise True.
            Default: False
        external_field: This is a key/value mapping of any additional
            information that can be gathered about the organization from the
            database it is being pulled from.  Some examples (but could really
            be anything):

            employee_count
            volunteer_count
            mission
            current_budget
            source_data - URL of where this data was sourced from

    """

    def __init__(self):
        """Initializes a new Organization."""
        self.id = None # type: Optional[Text]
        self._registration_country = None # type: Optional[Text]
        self._registration_id = None # type: Optional[Text]
        self._registrations = [] # type: List[Dict[Text, Text]]
        self.ids = {}
        self.name = None # type: Optional[Text]
        self.website = None # type: Optional[Text]
        self.mailing_address = {}
        self.phone = None # type: Optional[Text]
        self.year_founded = None # type: Optional[int]
        self.inactive = False # type: Optional[bool]
        self.external_field = {}
    
    def is_valid(self) -> bool: 
        """Checks if this organization is valid for importing.

        A valid organization is one that has an id, a name, and a registration
        (both the country and ID of registration).

        Returns:
            True if this organization is valid, otherwise False.
        
        """
        if (self.id is None or
            self.name is None or
            self._registration_country is None or
            self._registration_id is None
        ):
            return False
        return True

    def add_registration(self, registration_country: Text, registration_id: Text):
        """Add a government registration to this Organization.
        
        Add the given registration information to the organization record.
        The first registration that is added to an organization will be
        treated as the "primary" registration.

        All registration data is stored in the ``_registrations``, including
        the primary registration.  The primary registration will also be
        stored in the ``_registration_country`` and ``_registration_id`` fields.

        Args:
            registration_country: 2-letter country code of the country the
                registration is for.  Examples: "US", "GB".
                See: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements
            registration_id: The government registration ID. No spaces or
                hyphens should be included.  Letters should be un uppercase
                unless the registration ID is case sensitive (if the issuing
                government distinguishes between registrations with lowercase
                vs uppercase).

        """
        if self._registration_country is None:
            self._registration_country = registration_country
            self._registration_id = registration_id
        registration = {
            "country": registration_country,
            "id": registration_id
        }
        self._registrations.append(registration)

    def to_dict(self) -> Dict:
        """Creates a dict of this Organization that is suitable for being
        transformed to JSON and imported.
        
        """
        return_data = {
            "id": self.id,
            "registration_country": self._registration_country,
            "registation_id": self._registration_id,
            "registrations": self._registrations,
            "ids": self.ids,
            "name": self.name,
            "website": self.website,
            "mailing_address": self.mailing_address,
            "phone": self.phone,
            "year_founded": self.year_founded,
            "inactive": self.inactive or None
        }
        for key, value in self.external_field.items():
            return_data[key] = value
        return {key: value for key, value in return_data.items() if value}

    def __str__(self):
        output = "Organization {}".format(self.id or "[NO ID]")
        if self.name:
            output += "\n  Name: {}".format(self.name)
        if self._registration_country:
            output += "\n  Registration Country: {}".format(self._registration_country)
        if self._registration_id:
            output += "\n  Registration ID: {}". format(self._registration_id)
        return output

    def upload(self):
        """Stub method.

        When we run this in production, this function will be replaced with
        code that actually uplosds the organization record to GlobalGiving.

        """
        pass
