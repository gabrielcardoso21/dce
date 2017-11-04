# -*- coding: utf-8 -*-
# Copyright 2017 Gabriel Cardoso de Faria
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class Responsavel(models.Model):
    _name = 'responsavel'

    name = fields.Char(
        string=u'Nome',
    )

    eventos_responsavel = fields.Many2many(
        string=u'Festas que foi responsável',
        comodel_name='evento',
        inverse_name='responsaveis',
        relation='evento_responsavel_rel',
    )
    eventos_ouvidoria = fields.Many2many(
        string=u'Festas que foi de ouvidoria',
        comodel_name='evento',
        inverse_name='ouvidoria_ids',
        relation='evento_ouvidoria_rel',
    )

    sexo = fields.Selection(
        string=u'Sexo: ',
        selection=[
            ('masculino', 'Masculino'),
            ('feminino', 'Feminino'),
        ],
        default='masculino',
    )

    user_id = fields.Many2one(
        string=u'Usuario: ',
        comodel_name='res.users',
        ondelete='set null',
    )

