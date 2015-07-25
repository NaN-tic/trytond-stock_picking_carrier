#This file is part stock_picking_carrier module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta

__all__ = ['ShipmentOutPicking', 'ShipmentOutPickingResult', 'ShipmentOutPacked']
__metaclass__ = PoolMeta


class ShipmentOutPicking:
    __name__ = 'stock.shipment.out.picking'
    carrier = fields.Boolean('Carrier',
        help='Send shipment to API carrier')

    @staticmethod
    def default_carrier():
        return True


class ShipmentOutPickingResult:
    __name__ = 'stock.shipment.out.picking.result'
    label = fields.Binary('Label', filename='label_name')
    label_name = fields.Char('Label Name')


class ShipmentOutPacked:
    __name__ = 'stock.shipment.out.packed'

    @classmethod
    def __setup__(cls):
        super(ShipmentOutPacked, cls).__setup__()
        cls._error_messages.update({
            'not_label': 'Not return API "%(carrier)s" a label',
            })

    def transition_packed(self):
        pool = Pool()
        Shipment = pool.get('stock.shipment.out')

        super(ShipmentOutPacked, self).transition_packed()
        shipment = self.result.shipment

        # Send shipment to carrier API
        if self.picking.carrier and shipment.carrier:
            refs, labs, errs = Shipment.send_shipment_api(shipment)

            if labs:
                lab, = labs
                self.result.label = buffer(open(lab, "rb").read())
                self.result.label_name = lab.split('/')[2]
                return 'result'
            else:
                self.result.note = self.raise_user_error('not_label', {
                        'carrier': shipment.carrier.rec_name,
                        }, raise_exception=False)
        self.result.label = None
        self.result.label_name = None
        return 'result'

    def default_result(self, fields):
        res = super(ShipmentOutPacked, self).default_result(fields)
        res['label'] = self.result.label
        res['label_name'] =self.result.label_name
        return res
