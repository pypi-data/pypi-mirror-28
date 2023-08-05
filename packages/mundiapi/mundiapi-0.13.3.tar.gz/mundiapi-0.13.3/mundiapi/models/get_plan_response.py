# -*- coding: utf-8 -*-

"""
    mundiapi.models.get_plan_response

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io )
"""
from mundiapi.api_helper import APIHelper
import mundiapi.models.get_plan_item_response

class GetPlanResponse(object):

    """Implementation of the 'GetPlanResponse' model.

    Response object for getting a plan

    Attributes:
        id (string): TODO: type description here.
        name (string): TODO: type description here.
        description (string): TODO: type description here.
        url (string): TODO: type description here.
        statement_descriptor (string): TODO: type description here.
        interval (string): TODO: type description here.
        interval_count (int): TODO: type description here.
        billing_type (string): TODO: type description here.
        payment_methods (list of string): TODO: type description here.
        installments (list of int): TODO: type description here.
        status (string): TODO: type description here.
        currency (string): TODO: type description here.
        created_at (datetime): TODO: type description here.
        updated_at (datetime): TODO: type description here.
        items (list of GetPlanItemResponse): TODO: type description here.
        billing_days (list of int): TODO: type description here.
        shippable (bool): TODO: type description here.
        metadata (dict<object, string>): TODO: type description here.
        trial_period_days (int): TODO: type description here.
        minimum_price (int): TODO: type description here.
        deleted_at (datetime): TODO: type description here.

    """

    # Create a mapping from Model property names to API property names
    _names = {
        "id" : "id",
        "name" : "name",
        "description" : "description",
        "url" : "url",
        "statement_descriptor" : "statement_descriptor",
        "interval" : "interval",
        "interval_count" : "interval_count",
        "billing_type" : "billing_type",
        "payment_methods" : "payment_methods",
        "installments" : "installments",
        "status" : "status",
        "currency" : "currency",
        "created_at" : "created_at",
        "updated_at" : "updated_at",
        "items" : "items",
        "billing_days" : "billing_days",
        "shippable" : "shippable",
        "metadata" : "metadata",
        "trial_period_days" : "trial_period_days",
        "minimum_price" : "minimum_price",
        "deleted_at" : "deleted_at"
    }

    def __init__(self,
                 id=None,
                 name=None,
                 description=None,
                 url=None,
                 statement_descriptor=None,
                 interval=None,
                 interval_count=None,
                 billing_type=None,
                 payment_methods=None,
                 installments=None,
                 status=None,
                 currency=None,
                 created_at=None,
                 updated_at=None,
                 items=None,
                 billing_days=None,
                 shippable=None,
                 metadata=None,
                 trial_period_days=None,
                 minimum_price=None,
                 deleted_at=None):
        """Constructor for the GetPlanResponse class"""

        # Initialize members of the class
        self.id = id
        self.name = name
        self.description = description
        self.url = url
        self.statement_descriptor = statement_descriptor
        self.interval = interval
        self.interval_count = interval_count
        self.billing_type = billing_type
        self.payment_methods = payment_methods
        self.installments = installments
        self.status = status
        self.currency = currency
        self.created_at = APIHelper.RFC3339DateTime(created_at) if created_at else None
        self.updated_at = APIHelper.RFC3339DateTime(updated_at) if updated_at else None
        self.items = items
        self.billing_days = billing_days
        self.shippable = shippable
        self.metadata = metadata
        self.trial_period_days = trial_period_days
        self.minimum_price = minimum_price
        self.deleted_at = APIHelper.RFC3339DateTime(deleted_at) if deleted_at else None


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
        id = dictionary.get("id")
        name = dictionary.get("name")
        description = dictionary.get("description")
        url = dictionary.get("url")
        statement_descriptor = dictionary.get("statement_descriptor")
        interval = dictionary.get("interval")
        interval_count = dictionary.get("interval_count")
        billing_type = dictionary.get("billing_type")
        payment_methods = dictionary.get("payment_methods")
        installments = dictionary.get("installments")
        status = dictionary.get("status")
        currency = dictionary.get("currency")
        created_at = APIHelper.RFC3339DateTime.from_value(dictionary.get("created_at")).datetime if dictionary.get("created_at") else None
        updated_at = APIHelper.RFC3339DateTime.from_value(dictionary.get("updated_at")).datetime if dictionary.get("updated_at") else None
        items = None
        if dictionary.get("items") != None:
            items = list()
            for structure in dictionary.get("items"):
                items.append(mundiapi.models.get_plan_item_response.GetPlanItemResponse.from_dictionary(structure))
        billing_days = dictionary.get("billing_days")
        shippable = dictionary.get("shippable")
        metadata = dictionary.get("metadata")
        trial_period_days = dictionary.get("trial_period_days")
        minimum_price = dictionary.get("minimum_price")
        deleted_at = APIHelper.RFC3339DateTime.from_value(dictionary.get("deleted_at")).datetime if dictionary.get("deleted_at") else None

        # Return an object of this model
        return cls(id,
                   name,
                   description,
                   url,
                   statement_descriptor,
                   interval,
                   interval_count,
                   billing_type,
                   payment_methods,
                   installments,
                   status,
                   currency,
                   created_at,
                   updated_at,
                   items,
                   billing_days,
                   shippable,
                   metadata,
                   trial_period_days,
                   minimum_price,
                   deleted_at)


