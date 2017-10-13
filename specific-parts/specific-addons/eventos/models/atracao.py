# -*- coding: utf-8 -*-
# Copyright 2017 Gabriel Cardoso de Faria
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from ..funcoes_uteis import *
from dateutil.relativedelta import relativedelta

MESES = [
    ('01', 'Janeiro'),
    ('02', 'Fevereiro'),
    ('03', 'Março'),
    ('04', 'Abril'),
    ('05', 'Maio'),
    ('06', 'Junho'),
    ('07', 'Julho'),
    ('08', 'Agosto'),
    ('09', 'Setembro'),
    ('10', 'Outubro'),
    ('11', 'Novembro'),
    ('12', 'Dezembro'),
]


class Atracao(models.Model):
    _name = 'atracao'
    _order = 'data, id desc'
    _rec_name = 'display_name'
    
    @api.multi
    @api.depends('festa_id', 'artista_id', 'data_fmt')
    def _compute_display_name(self):
        for atracao in self:
            display_name = '%s - %s - %s' % (atracao.festa_id or '',
                                             atracao.artista_id.name or '',
                                             atracao.data_fmt or '')
            atracao.display_name = display_name
    
    @api.multi
    @api.depends('data')
    def _compute_data_fmt(self):
        for atracao in self:
            if atracao.data:
                atracao.dia = atracao.data[8:]
                atracao.mes = dict(MESES)[atracao.data[5:7]]
                atracao.ano = atracao.data[:4]
                data = fields.Date.from_string(atracao.data)
                data += relativedelta(days=1)
                atracao.data_fmt = data.strftime('%d/%m/%Y')
                
    @api.multi
    @api.depends('horario_inicio', 'horario_termino')
    def _compute_horarios(self):
        for atracao in self:
            if atracao.horario_inicio:
                atracao.inicio_fmt = float_to_time(atracao.horario_inicio)
            if atracao.horario_termino:
                atracao.termino_fmt = float_to_time(atracao.horario_termino)
                
    @api.multi
    @api.depends('horario_passagem')
    def _compute_passagem_som(self):
        for atracao in self:
            if atracao.horario_passagem:
                atracao.passagem_fmt = float_to_time(atracao.horario_passagem)
                data_passagem = fields.Date.from_string(atracao.data)
                atracao.data_passagem_fmt = data_passagem.strftime('%d/%m/%Y')
                
    @api.multi
    @api.depends('cache')
    def _compute_cache_fmt(self):
        for atracao in self:
            if atracao.cache:
                atracao.cache_fmt = str(atracao.cache).replace('.', ',')
    
    display_name = fields.Char(
        string=u'Nome do registro',
        compute='_compute_display_name',
        store=True,
    )
    data_fmt = fields.Char(
        string=u'Data formatada',
        compute='_compute_data_fmt',
    )
    dia = fields.Char(
        string=u'Dia',
        compute='_compute_data_fmt',
    )
    mes = fields.Char(
        string=u'Mes',
        compute='_compute_data_fmt',
    )
    ano = fields.Char(
        string=u'Mes',
        compute='_compute_data_fmt',
    )
    inicio_fmt = fields.Char(
        string=u'Horário de início formatado',
        compute='_compute_horarios',
    )
    termino_fmt = fields.Char(
        string=u'Horário de término formatado',
        compute='_compute_horarios',
    )
    passagem_fmt = fields.Char(
        string=u'Horário de passagem de som',
        compute='_compute_passagem_som',
    )
    data_passagem_fmt = fields.Char(
        string=u'Data da passagem de som',
        compute='_compute_passagem_som',
    )
    cache_fmt = fields.Char(
        string=u'Cache formatado',
        compute='_compute_cache_fmt',
    )

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
    horario_passagem = fields.Float(
        string=u'Horário da passagem de som',
        digits=(2, 2),
    )
    cache = fields.Float(
        string=u'Cache: ',
        digits=(16, 2),
    )
    cache_ext = fields.Char(
        string=u'Por extenso: ',
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


