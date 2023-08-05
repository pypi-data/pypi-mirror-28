# -*- coding: utf-8 -*-

"""
    mundiapi.mundi_api_client

    This file was automatically generated by APIMATIC v2.0 ( https://apimatic.io ).
"""
from .decorators import lazy_property
from .configuration import Configuration
from .controllers.charges_controller import ChargesController
from .controllers.customers_controller import CustomersController
from .controllers.invoices_controller import InvoicesController
from .controllers.plans_controller import PlansController
from .controllers.subscriptions_controller import SubscriptionsController
from .controllers.orders_controller import OrdersController
from .controllers.tokens_controller import TokensController
from .controllers.recipients_controller import RecipientsController
from .controllers.sellers_controller import SellersController

class MundiapiClient(object):

    config = Configuration

    @lazy_property
    def charges(self):
        return ChargesController()

    @lazy_property
    def customers(self):
        return CustomersController()

    @lazy_property
    def invoices(self):
        return InvoicesController()

    @lazy_property
    def plans(self):
        return PlansController()

    @lazy_property
    def subscriptions(self):
        return SubscriptionsController()

    @lazy_property
    def orders(self):
        return OrdersController()

    @lazy_property
    def tokens(self):
        return TokensController()

    @lazy_property
    def recipients(self):
        return RecipientsController()

    @lazy_property
    def sellers(self):
        return SellersController()


    def __init__(self, 
                 basic_auth_user_name = None,
                 basic_auth_password = None):
        if basic_auth_user_name != None:
            Configuration.basic_auth_user_name = basic_auth_user_name
        if basic_auth_password != None:
            Configuration.basic_auth_password = basic_auth_password


