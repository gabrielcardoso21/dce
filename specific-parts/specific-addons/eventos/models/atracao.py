# -*- coding: utf-8 -*-
# Copyright 2017 Gabriel Cardoso de Faria
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class Atracao(models.Model):
    _name = 'atracao'
    _order = 'data, id desc'

    festa_id = fields.Many2one(
        string=u'Festa: ',
        comodel_name='evento',
    )
    artista_id = fields.Many2one(
        string=u'Artista: ',
        comodel_name='artista',
    )
    tipo_artista = fields.Selection(
        related='artista_id.tipo'
    )
    estilo_musical = fields.Selection(
        related='artista_id.estilo_musical'
    )
    data = fields.Date(
        string=u'Data: ',
        related='festa_id.data',
    )
    local = fields.Selection(
        string=u'Local: ',
        selection=[
            ('pista', u'Pista'),
            ('cultural', u'Cultural'),
            ('rancho', u'Rancho'),
        ],
    )
    horario_inicio = fields.Float(
        string=u'Horário de Início: ',
        digits=(2, 2),
    )
    horario_termino = fields.Float(
        string=u'Horário de Término: ',
        digits=(2, 2),
    )
    cache = fields.Float(
        string=u'Cache: ',
        digits=(16, 2),
    )
    data_extra_combinada = fields.Boolean(
        string=u'Data extra combinada?',
    )
    responsavel_id = fields.Many2one(
        string=u'Responsável: ',
        comodel_name='responsavel',
    )
    lanches = fields.Integer(
        string=u'Lanches: ',
    )
    cortesias = fields.Integer(
        string=u'Cortesias: ',
        default=0,
    )
    consumacao = fields.Selection(
        string=u'Consumação: ',
        selection=[
            ('padrao', 'Padrão'),
            ('especial', 'Especial'),
        ],
        default='padrao',
    )
    detalhes_consumacao = fields.Char(
        string=u'Detalhes da consumação: ',
    )

    @api.onchange('artista_id')
    def get_informacoes_padrao(self):
        if self.artista_id:
            self.lanches = self.artista_id.integrantes
            self.cortesias = self.artista_id.cortesias


