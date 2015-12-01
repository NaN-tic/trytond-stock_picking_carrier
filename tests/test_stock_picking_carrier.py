# This file is part of the stock_picking_carrier module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class StockPickingCarrierTestCase(ModuleTestCase):
    'Test Stock Picking Carrier module'
    module = 'stock_picking_carrier'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        StockPickingCarrierTestCase))
    return suite