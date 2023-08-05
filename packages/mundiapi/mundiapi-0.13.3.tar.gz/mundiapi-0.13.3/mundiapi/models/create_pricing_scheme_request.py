# -*- coding: utf-8 -*-

"""
    mundiapi.models.create_pricing_scheme_request

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io )
"""
import mundiapi.models.create_price_bracket_request

class CreatePricingSchemeRequest(object):

    """Implementation of the 'CreatePricingSchemeRequest' model.

    Request for creating a pricing scheme

    Attributes:
        scheme_type (string): Scheme type
        price_brackets (list of CreatePriceBracketRequest): Price brackets
        price (int): Price
        minimum_price (int): Minimum price

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "scheme_type" : "scheme_type",
        "price_brackets" : "price_brackets",
        "price" : "price",
        "minimum_price" : "minimum_price"
    }

    def __init__(self,
                 scheme_type=None,
                 price_brackets=None,
                 price=None,
                 minimum_price=None):
        """Constructor for the CreatePricingSchemeRequest class"""

        # Initialize members of the class
        self.scheme_type = scheme_type
        self.price_brackets = price_brackets
        self.price = price
        self.minimum_price = minimum_price


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
        scheme_type = dictionary.get("scheme_type")
        price_brackets = None
        if dictionary.get("price_brackets") != None:
            price_brackets = list()
            for structure in dictionary.get("price_brackets"):
                price_brackets.append(mundiapi.models.create_price_bracket_request.CreatePriceBracketRequest.from_dictionary(structure))
        price = dictionary.get("price")
        minimum_price = dictionary.get("minimum_price")

        # Return an object of this model
        return cls(scheme_type,
                   price_brackets,
                   price,
                   minimum_price)


