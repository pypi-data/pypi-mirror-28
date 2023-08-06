# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2018 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Views for label batches
"""

from __future__ import unicode_literals, absolute_import

from rattail.db import model

from webhelpers2.html import HTML, tags

from tailbone.views.batch import BatchMasterView3 as BatchMasterView


class LabelBatchView(BatchMasterView):
    """
    Master view for label batches.
    """
    model_class = model.LabelBatch
    model_row_class = model.LabelBatchRow
    default_handler_spec = 'rattail.batch.labels:LabelBatchHandler'
    model_title_plural = "Label Batches"
    route_prefix = 'labels.batch'
    url_prefix = '/labels/batches'
    template_prefix = '/batch/labels'
    creatable = False
    rows_editable = True
    rows_bulk_deletable = True
    cloneable = True
    results_executable = True

    row_grid_columns = [
        'sequence',
        'upc',
        'brand_name',
        'description',
        'size',
        'regular_price',
        'sale_price',
        'label_profile',
        'label_quantity',
        'status_code',
    ]

    form_fields = [
        'id',
        'description',
        'static_prices',
        'notes',
        'created',
        'created_by',
        'handheld_batches',
        'rowcount',
        'executed',
        'executed_by',
    ]

    def configure_form(self, f):
        super(LabelBatchView, self).configure_form(f)

        # handheld_batches
        f.set_readonly('handheld_batches')
        f.set_renderer('handheld_batches', self.render_handheld_batches)

        if self.viewing or self.deleting:
            batch = self.get_instance()
            if not batch._handhelds:
                f.remove_field('handheld_batches')

    def render_handheld_batches(self, label_batch, field):
        items = ''
        for handheld in label_batch._handhelds:
            text = handheld.handheld.id_str
            url = self.request.route_url('batch.handheld.view', uuid=handheld.handheld_uuid)
            items += HTML.tag('li', c=tags.link_to(text, url))
        return HTML.tag('ul', c=items)

    def configure_row_grid(self, g):
        super(LabelBatchView, self).configure_row_grid(g)
        g.set_label('upc', "UPC")
        g.set_label('brand_name', "Brand")
        g.set_label('regular_price', "Reg Price")
        g.set_label('label_profile', "Label Type")
        g.set_label('label_quantity', "Qty")

    def row_grid_extra_class(self, row, i):
        if row.status_code != row.STATUS_OK:
            return 'warning'

    def _preconfigure_row_fieldset(self, fs):
        fs.sequence.set(readonly=True)
        fs.product.set(readonly=True)
        fs.upc.set(readonly=True, label="UPC")
        fs.brand_name.set(readonly=True)
        fs.description.set(readonly=True)
        fs.size.set(readonly=True)
        fs.department_number.set(readonly=True)
        fs.department_name.set(readonly=True)
        fs.regular_price.set(readonly=True)
        fs.pack_quantity.set(readonly=True)
        fs.pack_price.set(readonly=True)
        fs.sale_price.set(readonly=True)
        fs.sale_start.set(readonly=True)
        fs.sale_stop.set(readonly=True)
        fs.vendor_id.set(readonly=True, label="Vendor ID")
        fs.vendor_name.set(readonly=True)
        fs.vendor_item_code.set(readonly=True)
        fs.case_quantity.set(readonly=True)
        fs.status_code.set(readonly=True)
        fs.status_text.set(readonly=True)

        fs.label_profile.set(label="Label Type")

    def configure_row_fieldset(self, fs):
        if self.viewing:
            fs.configure(
                include=[
                    fs.sequence,
                    fs.upc,
                    fs.brand_name,
                    fs.description,
                    fs.size,
                    fs.department_number,
                    fs.department_name,
                    fs.regular_price,
                    fs.pack_quantity,
                    fs.pack_price,
                    fs.sale_price,
                    fs.sale_start,
                    fs.sale_stop,
                    fs.vendor_id,
                    fs.vendor_name,
                    fs.vendor_item_code,
                    fs.case_quantity,
                    fs.label_profile,
                    fs.label_quantity,
                    fs.status_code,
                    fs.status_text,
                ])

        elif self.editing:
            fs.configure(
                include=[
                    fs.sequence,
                    fs.upc,
                    fs.product,
                    fs.department_number,
                    fs.department_name,
                    fs.regular_price,
                    fs.sale_price,
                    fs.label_profile,
                    fs.label_quantity,
                    fs.status_code,
                    fs.status_text,
                ])


def includeme(config):
    LabelBatchView.defaults(config)
