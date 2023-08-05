# -*- coding: utf-8 -*-

"""
    mundiapi.models.update_price_bracket_request

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io )
"""


class UpdatePriceBracketRequest(object):

    """Implementation of the 'UpdatePriceBracketRequest' model.

    Request for updating a price bracket

    Attributes:
        start_quantity (int): Start quantity of the bracket
        price (int): Price
        end_quantity (int): End quantity of the bracket
        overage_price (int): Overage price

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "start_quantity" : "start_quantity",
        "price" : "price",
        "end_quantity" : "end_quantity",
        "overage_price" : "overage_price"
    }

    def __init__(self,
                 start_quantity=None,
                 price=None,
                 end_quantity=None,
                 overage_price=None):
        """Constructor for the UpdatePriceBracketRequest class"""

        # Initialize members of the class
        self.start_quantity = start_quantity
        self.price = price
        self.end_quantity = end_quantity
        self.overage_price = overage_price


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
        start_quantity = dictionary.get("start_quantity")
        price = dictionary.get("price")
        end_quantity = dictionary.get("end_quantity")
        overage_price = dictionary.get("overage_price")

        # Return an object of this model
        return cls(start_quantity,
                   price,
                   end_quantity,
                   overage_price)


