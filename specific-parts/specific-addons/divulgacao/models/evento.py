# -*- coding: utf-8 -*-
# Copyright 2017 Gabriel Cardoso de Faria
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class Evento(models.Model):
    _inherit = 'evento'

    @api.multi
    def confirmar_evento(self):
        super(Evento, self).confirmar_evento()
        users = self.env['res.groups'].search([
            ('id', '=', self.env.ref('divulgacao.group_divulgacao').id),
        ]).mapped('users')
        subtype = self.env.ref('mail.mt_note')
        self.message_subscribe_users(user_ids=users.ids, subtype_ids=subtype.ids)
        self.message_post(body="Novo evento confirmado: "+self.name+".")
