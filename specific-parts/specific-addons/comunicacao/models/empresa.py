# -*- coding: utf-8 -*-
# Copyright 2017 Gabriel Cardoso de Faria
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class Empresa(models.Model):
    
    _name = 'empresa'
    _description = 'Empresa de Design'
    
    name = fields.Char(
        string=u'Nome',
    )
