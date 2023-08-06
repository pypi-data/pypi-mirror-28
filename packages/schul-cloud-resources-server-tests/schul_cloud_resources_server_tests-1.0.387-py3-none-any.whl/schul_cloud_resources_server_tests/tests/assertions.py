"""This module contains assertions which work across many tests.

These assertions are a bit more complex than an assert ==.
"""

import json
from schul_cloud_resources_server_tests.errors import errors as server_errors
import sys
from schul_cloud_resources_api_v1.schema import get_schemas
from pprint import pprint

if sys.version_info[0] == 2:
    STRING_TYPE = basestring
else:
    STRING_TYPE = str


def to_dict(model):
    """Return a dictionary."""
    if hasattr(model, "to_dict"):
        return model.to_dict()
    try:
        if hasattr(model, "json"):
            return model.json()
        if isinstance(model, STRING_TYPE):
            return json.loads(model)
    except ValueError as error:
        raise ValueError("The response should be JSON. {}".format(error))
    assert isinstance(model, dict)
    return model


def assertIsResponse(response, link_self="TODO"):
    response = to_dict(response)
    assert ("errors" in response) ^ ("data" in response), "Either the member \"data\" or the member \"errors\" must be given. http://jsonapi.org/format/#conventions"
    assert ("data" in response if "included" in response else True), "If a document does not contain a top-level data key, the included member MUST NOT be present either. http://jsonapi.org/format/#conventions"
    assert "jsonapi" in response, "jsonapi must be present, see the api specification."
    jsonapi = response.get("jsonapi")
    assert jsonapi is not None, "the jsonapi attribute must be set in the reponse"
    assert jsonapi.get("version") == "1.0", "version must be present http://jsonapi.org/format/#document-jsonapi-object"
    assert "meta" in jsonapi, "meta tag should be present to contain some information."
    for attr in ["name", "source", "description"]:
        assert attr in jsonapi["meta"], "{} must be present, see #/definition/Jsonapi".format(attr)
        assert isinstance(jsonapi["meta"][attr], STRING_TYPE), "jsonapi.meta.{} must be a string.".format(attr)
    if link_self is not None:
       assert link_self != "TODO", "Change the test case source code to include the url."
       assert "links" in response
       assert isinstance(response["links"], dict)
       assert "self" in response["links"] or "_self" in response["links"]
       link = response["links"].get("self", response["links"].get("_self"))
       assert link == link_self, '{} == {}'.format(link, link_self)


def assertIsError(response, status):
    """This is an error response object with a specific status code.

    You can view the specification here:
    - https://github.com/schul-cloud/resources-api-v1/blob/f0ce9acfde59563822071207bd176baf648db8b4/api-definition/swagger.yaml#L292
    - updated: https://github.com/schul-cloud/resources-api-v1/blob/master/api-definition/swagger.yaml#L292
    - Error specification:
    """
    response = to_dict(response)
    pprint(("response:", response))
    assertIsResponse(response, None)
    get_schemas()["error"].validate(response)
    error = response["errors"][0]
    assert error["status"] == str(status), "{} == {}".format(repr(error["status"]), repr(str(status)))
