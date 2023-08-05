# -*- coding: utf-8 -*-

"""
    mundiapi.models.list_seller_response

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io )
"""
import mundiapi.models.get_seller_response
import mundiapi.models.paging_response

class ListSellerResponse(object):

    """Implementation of the 'ListSellerResponse' model.

    TODO: type model description here.

    Attributes:
        data (list of GetSellerResponse): The order object
        paging (PagingResponse): Paging object

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "data" : "data",
        "paging" : "paging"
    }

    def __init__(self,
                 data=None,
                 paging=None):
        """Constructor for the ListSellerResponse class"""

        # Initialize members of the class
        self.data = data
        self.paging = paging


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
        data = None
        if dictionary.get("data") != None:
            data = list()
            for structure in dictionary.get("data"):
                data.append(mundiapi.models.get_seller_response.GetSellerResponse.from_dictionary(structure))
        paging = mundiapi.models.paging_response.PagingResponse.from_dictionary(dictionary.get("paging")) if dictionary.get("paging") else None

        # Return an object of this model
        return cls(data,
                   paging)


