# Organization Parser

A python library for importing parsed organization data, into GlobalGiving.

All parsed data should be put into a `Organization` object.  An internal tool can then be used to actually insert the data into a database.

## Setup

1. Clone this repo
1. Determine the "short name" for the data source you will be parsing.  For example:
    * `gbchc` could be for British Charity Commision data
    * `za` for data from the South African government
    * For country codes, see: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements
1. Create a new file named `SHORTNAME_parser.py`

   ```python
    from globalgiving_utilities import Organization
    ```
1. Write code to parse the new data (and possibly download it, though you can also assume that someone will manually download a new copy of it each time)
1. Set the new organizations to have an id of `o.SHORTNAME.####` (More on this in the pydoc of organization.py)
1. Clean up the organization name to be in "Title Case".
1. Set the new organizations to have a source of the same value as the "short name".
1. If there is a website URL for each organization, ensure they begin with `http://` or `https://`.
1. Ensure these minimum fields are filled out for every organization:
    * id
    * name
    * registration id
    * registration country
    * source
1. Write tests to cover your code and ensure it is working properly

## How To Use `organization.py`

Look in [organization.py](globalgiving_utilities/organization.py) and read the pydoc in there.  Usage of the `Organization` object is fully covered in there.

You can also look at the included example.

## Example

There is an example in [example_parser.py](example_parser.py).  The example shows how to utilize the Organization object and how to properly test your parser.