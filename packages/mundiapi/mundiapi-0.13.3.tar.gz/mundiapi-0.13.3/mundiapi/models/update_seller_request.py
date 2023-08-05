# -*- coding: utf-8 -*-

"""
    mundiapi.models.update_seller_request

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io )
"""
import mundiapi.models.create_address_request

class UpdateSellerRequest(object):

    """Implementation of the 'UpdateSellerRequest' model.

    TODO: type model description here.

    Attributes:
        name (string): Seller name
        code (string): Seller code
        description (string): Seller description
        document (string): Seller document CPF or CNPJ
        status (string): TODO: type description here.
        mtype (string): TODO: type description here.
        address (CreateAddressRequest): TODO: type description here.
        metadata (dict<object, string>): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "name" : "name",
        "code" : "code",
        "description" : "description",
        "document" : "document",
        "status" : "status",
        "mtype" : "type",
        "address" : "address",
        "metadata" : "metadata"
    }

    def __init__(self,
                 name=None,
                 code=None,
                 description=None,
                 document=None,
                 status=None,
                 mtype=None,
                 address=None,
                 metadata=None):
        """Constructor for the UpdateSellerRequest class"""

        # Initialize members of the class
        self.name = name
        self.code = code
        self.description = description
        self.document = document
        self.status = status
        self.mtype = mtype
        self.address = address
        self.metadata = metadata


    @classmethod
    def from_dictionary(cls,
                        dictionary):
        """Creates an instance of this model from a dictionary

        Args:
            dictionary (dictionary): A dictionary representation of the object as
            obtained from the deserialization of the server's response. The keys
            MUST match property names in the API description.

        Returns:
            object: An instance of this structure class.

        """
        if dictionary is None:
            return None

        # Extract variables from the dictionary
        name = dictionary.get("name")
        code = dictionary.get("code")
        description = dictionary.get("description")
        document = dictionary.get("document")
        status = dictionary.get("status")
        mtype = dictionary.get("type")
        address = mundiapi.models.create_address_request.CreateAddressRequest.from_dictionary(dictionary.get("address")) if dictionary.get("address") else None
        metadata = dictionary.get("metadata")

        # Return an object of this model
        return cls(name,
                   code,
                   description,
                   document,
                   status,
                   mtype,
                   address,
                   metadata)


