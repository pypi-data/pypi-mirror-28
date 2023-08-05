# -*- coding: utf-8 -*-
# Copyright 2016 Cédric Pigeon
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import mock

from odoo.addons.connector_lengow.tests import common
from odoo.exceptions import ValidationError
from odoo.osv.expression import TRUE_LEAF


class TestStock20(common.SetUpLengowBase20):

    def setUp(self):
        super(TestStock20, self).setUp()
        self.json_data.update({
            'fnac_update': {
                'status_code': 200,
                'json': {}}})
        order_message = self.json_data['orders']['json']
        order_data = order_message['orders'][0]
        order_data['marketplace'] = 'fnac'
        self.marketplace.write({'lengow_id': 'fnac'})
        with self.backend.work_on('lengow.sale.order') as work:
            sale_importer = work.component(usage='record.importer')
            sale_importer.run('999-2121515-6705141', order_data)
        order = self.env['sale.order'].search([('client_order_ref',
                                                '=',
                                                '999-2121515-6705141')])
        self.env['automatic.workflow.job'].run()
        self.assertEqual(order.state, 'sale')
        self.picking = order.picking_ids[0]

    def test_export_picking_done_no_tracking(self):
        with mock.patch(self.post_method) as mock_post:
            mock_post = self._configure_mock_request('fnac_update',
                                                     mock_post)
            with self.assertRaises(ValidationError):
                # For Fnac tracking information are mandatory
                self.picking.force_assign()
                self.picking.do_transfer()

                self.assertEqual(len(self.picking.lengow_bind_ids), 1)

                jobs = self.env['queue.job'].search([TRUE_LEAF])

                self.assertEqual(len(jobs), 1)
                self.assertEqual(
                    jobs.name,
                    'Export Lengow Picking %s (Order: '
                    'AMAZON-999-2121515-6705141)' % self.picking.name)

                with self.backend.work_on('lengow.stock.picking') as work:
                    exporter = work.component(usage='record.exporter')
                    exporter.run(self.picking.lengow_bind_ids.id)

                mock_post.assert_called_with(
                    'http://anywsdlurl/fnac/99128/999-2121515-6705141'
                    '/Shipped.xml', params={}, data={}, headers={})

    def test_export_picking_done_tracking(self):
        with mock.patch(self.post_method) as mock_post:
            mock_post = self._configure_mock_request('fnac_update',
                                                     mock_post)

            carrier = self.env.ref('connector_lengow_fnac.carrier_fnac_ups')
            self.picking.write({'carrier_tracking_ref': 'tracking code test',
                                'carrier_id': carrier.id})
            self.picking.force_assign()
            self.picking.do_transfer()

            with self.backend.work_on('lengow.stock.picking') as work:
                exporter = work.component(usage='record.exporter')
                exporter.run(self.picking.lengow_bind_ids.id)
            mock_post.assert_called_with(
                'http://anywsdlurl/fnac/99128/999-2121515-6705141'
                '/Shipped.xml',
                params={'trackingColis': 'tracking code test',
                        'transporteurColis': 'UPS'},
                data={}, headers={})
