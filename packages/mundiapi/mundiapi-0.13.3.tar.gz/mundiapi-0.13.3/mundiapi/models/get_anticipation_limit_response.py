# -*- coding: utf-8 -*-

"""
    mundiapi.models.get_anticipation_limit_response

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io )
"""


class GetAnticipationLimitResponse(object):

    """Implementation of the 'GetAnticipationLimitResponse' model.

    Anticipation limit

    Attributes:
        amount (int): Amount
        anticipation_fee (int): Anticipation fee

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "amount" : "amount",
        "anticipation_fee" : "anticipation_fee"
    }

    def __init__(self,
                 amount=None,
                 anticipation_fee=None):
        """Constructor for the GetAnticipationLimitResponse class"""

        # Initialize members of the class
        self.amount = amount
        self.anticipation_fee = anticipation_fee


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
        amount = dictionary.get("amount")
        anticipation_fee = dictionary.get("anticipation_fee")

        # Return an object of this model
        return cls(amount,
                   anticipation_fee)


