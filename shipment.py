#This file is part stock_picking_carrier module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
import tarfile
import tempfile
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all__ = ['ShipmentOutPicking', 'ShipmentOutPickingResult', 'ShipmentOutPacked',
    'ShipmentOutScanningStart', 'ShipmentOutScanningResult', 'ShipmentOutScanning']


class ShipmentOutPicking(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.picking'
    carrier = fields.Boolean('Carrier',
        help='Send shipment to API carrier')

    @staticmethod
    def default_carrier():
        return True


class ShipmentOutPickingResult(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.picking.result'
    label = fields.Binary('Label', filename='label_name')
    label_name = fields.Char('Label Name')


class ShipmentOutPacked(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.packed'

    def transition_packed(self):
        Shipment = Pool().get('stock.shipment.out')

        super(ShipmentOutPacked, self).transition_packed()
        shipment = self.result.shipment
        dbname = Transaction().database.name

        # Send shipment to carrier API
        if self.picking.carrier and shipment.carrier:
            refs, labs, errs = Shipment.send_shipment_api(shipment)

            if labs:
                if len(labs) > 1:
                    temp = tempfile.NamedTemporaryFile(
                        prefix='%s-carrier-' % dbname, delete=False)
                    temp.close()
                    with tarfile.open(temp.name, "w:gz") as tar:
                        for path_label in labs:
                            tar.add(path_label)
                    tar.close()
                    label = fields.Binary.cast(open(temp.name, "rb").read())
                    label_name = '%s.tgz' % temp.name.split('/')[2]
                else:
                    lab, = labs
                    label = fields.Binary.cast(open(lab, "rb").read())
                    label_name = lab.split('/')[2]
                self.result.labs = labs
                self.result.label = label
                self.result.label_name = label_name
                return 'result'
            else:
                self.result.note += gettext('stock_picking_carrier.msg_not_label',
                    carrier=shipment.carrier.rec_name)

        # labs is not a file in packed result; we use in extra modules labs file
        self.result.labs = None
        self.result.label = None
        self.result.label_name = None
        return 'result'

    def default_result(self, fields):
        res = super(ShipmentOutPacked, self).default_result(fields)
        res['label'] = self.result.label
        res['label_name'] =self.result.label_name
        return res


class ShipmentOutScanningStart(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.scanning.start'
    carrier = fields.Boolean('Carrier',
        help='Send shipment to API carrier')

    @staticmethod
    def default_carrier():
        return True


class ShipmentOutScanningResult(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.scanning.result'
    label = fields.Binary('Label', filename='label_name')
    label_name = fields.Char('Label Name')


class ShipmentOutScanning(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.scanning'

    def transition_packed(self):
        Shipment = Pool().get('stock.shipment.out')

        packed = super(ShipmentOutScanning, self).transition_packed()
        if packed == 'start':
            return 'start'
        shipment = self.result.shipment

        # Send shipment to carrier API
        if self.start.carrier and shipment.carrier:
            refs, labs, errs = Shipment.send_shipment_api(shipment)

            if labs:
                lab, = labs
                self.result.labs = labs
                self.result.label = fields.Binary.cast(open(lab, "rb").read())
                self.result.label_name = lab.split('/')[2]
                return 'result'
            else:
                self.result.note += gettext('stock_picking_carrier.msg_not_label',
                    carrier=shipment.carrier.rec_name)
        self.result.labs = None
        self.result.label = None
        self.result.label_name = None
        return 'result'

    def default_result(self, fields):
        res = super(ShipmentOutScanning, self).default_result(fields)
        res['label'] = self.result.label
        res['label_name'] =self.result.label_name
        return res
