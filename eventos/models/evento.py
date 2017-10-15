# -*- coding: utf-8 -*-
# Copyright 2017 Gabriel Cardoso de Faria
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class Evento(models.Model):

    _name = 'evento'
    _description = 'Evento'

    name = fields.Char(
        string=u'Nome da Festa: ',
    )
    publico_alvo = fields.Selection(
        string=u'Público alvo: ',
        selection=[
            ('unifei', 'UNIFEI'),
            ('universitarios', 'Universitários'),
            ('itajubenses', 'Itajuebenses'),
            ('unifei_itajubenses', 'UNIFEI/Itajubenses'),
        ],
        default='unifei',
    )
    tematica = fields.Char(
        string=u'Temática: ',
    )
    data = fields.Date(
        string=u'Data: ',
    )
    horario_inicio = fields.Float(
        string=u'Início: ',
        digits=(2, 2),
    )
    horario_termino = fields.Float(
        string=u'Término: ',
        digits=(2, 2),
    )

    abre_pista = fields.Boolean(
        string=u'Abre Pista?',
        default=False,
    )
    abre_cultural = fields.Boolean(
        string=u'Abre Cultural?',
        default=True,
    )
    abre_rancho = fields.Boolean(
        string=u'Abre Rancho?',
        default=False,
    )
    atracao_pista_ids = fields.One2many(
        string=u'Atrações da Pista',
        comodel_name='atracao',
        inverse_name='festa_id',
        domain=[('local', '=', 'pista')],
    )
    atracao_cultural_ids = fields.One2many(
        string=u'Atrações do Cultural',
        comodel_name='atracao',
        inverse_name='festa_id',
        domain=[('local', '=', 'cultural')],
    )
    atracao_rancho_ids = fields.One2many(
        string=u'Atrações da Rancho',
        comodel_name='atracao',
        inverse_name='festa_id',
        domain=[('local', '=', 'rancho')],
    )
    state = fields.Selection(
        string=u'Status',
        selection=[
            ('provisorio', u'Provisório'),
            ('confirmado', u'Confirmado'),
        ],
        default='provisorio',
    )

    custo_total = fields.Float(
        string=u'Custo total da festa: ',
        digits=(16, 2),
        compute='_compute_custo_total',
    )
    responsaveis = fields.Many2many(
        string=u'Responsáveis',
        comodel_name='responsavel',
        inverse_name='eventos_responsavel',
        relation='evento_responsavel_rel',
    )
    ouvidoria_ids = fields.Many2many(
        string=u'Ouvidoria',
        comodel_name='responsavel',
        inverse_name='eventos_ouvidoria',
        relation='evento_ouvidoria_rel',
        domain=[('sexo', '=', 'feminino')]
    )
    promocao = fields.Text(
        string=u'Promoção',
    )
    decoracao = fields.Text(
        string=u'Decoração',
    )
    fotografo = fields.Boolean(
        string=u'Fotógrafo',
    )
    portaria_socio = fields.Float(
        string=u'Sócio: ',
        digits=(16, 2),
        default=0.00,
    )
    portaria_estudante = fields.Float(
        string=u'Estudante: ',
        digits=(16, 2),
        default=0.00,
    )
    portaria_nao_estudante = fields.Float(
        string=u'Não estudante: ',
        digits=(16, 2),
        default=0.00,
    )

    @api.depends('atracao_pista_ids.cache',
                 'atracao_cultural_ids.cache',
                 'atracao_rancho_ids.cache')
    def _compute_custo_total(self):
        for evento in self:
            custo_total = 0.00
            if evento.abre_pista and evento.atracao_pista_ids:
                custo_total += 1200.00
                for atracao in evento.atracao_pista_ids:
                    custo_total += atracao.cache
            if evento.abre_cultural and evento.atracao_cultural_ids:
                custo_total += 200.00
                for atracao in evento.atracao_cultural_ids:
                    custo_total += atracao.cache
            if evento.abre_rancho and evento.atracao_rancho_ids:
                custo_total += 0.00
                for atracao in evento.atracao_rancho_ids:
                    custo_total += atracao.cache
            evento.custo_total = custo_total

    @api.multi
    def confirmar_evento(self):
        for evento in self:
            evento.state = 'confirmado'

