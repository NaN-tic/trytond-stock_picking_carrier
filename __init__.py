#This file is part stock_picking_carrier module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import Pool
from .shipment import *

def register():
    Pool.register(
        ShipmentOutPicking,
        ShipmentOutPickingResult,
        module='stock_picking_carrier', type_='model')
    Pool.register(
        ShipmentOutPacked,
        module='stock_picking_carrier', type_='wizard')
