#This file is part stock_picking_carrier module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import Pool
from . import shipment

def register():
    Pool.register(
        shipment.ShipmentOutPicking,
        shipment.ShipmentOutPickingResult,
        shipment.ShipmentOutScanningStart,
        shipment.ShipmentOutScanningResult,
        module='stock_picking_carrier', type_='model')
    Pool.register(
        shipment.ShipmentOutPacked,
        shipment.ShipmentOutScanning,
        module='stock_picking_carrier', type_='wizard')
