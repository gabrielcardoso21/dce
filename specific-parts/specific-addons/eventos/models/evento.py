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
    )
    ouvidoria_ids = fields.Many2many(
        string=u'Ouvidoria',
        comodel_name='responsavel',
        inverse_name='eventos_ouvidoria',
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


class Artista(models.Model):
    _name = 'artista'

    apresentacao_ids = fields.One2many(
        string=u'Apresentações: ',
        comodel_name='atracao',
        inverse_name='artista_id'
    )
    name = fields.Char(
        string=u'Nome Artístico: '
    )
    tipo = fields.Selection(
        string=u'Tipo de músico: ',
        selection=[
            ('banda', u'Banda'),
            ('dj', u'DJ'),
        ]
    )
    estilo_musical = fields.Selection(
        string=u'Estilo Musical: ',
        selection=[
            ('funk', u'Funk'),
            ('eletronico', u'Eletrônico'),
            ('funk_eletronico', u'Funk/Eletrônico'),
            ('sertanejo', u'Sertanejo'),
            ('pop', u'Pop'),
            ('pop_rock', u'Pop/Rock'),
            ('samba_rock', u'Samba/Rock'),
            ('rock', u'Rock'),
            ('axe', u'Axé'),
            ('pagode', u'Pagode'),
            ('groove', u'Groove'),
        ],
    )
    integrantes = fields.Integer(
        string=u'Integrantes: ',
    )
    cortesias = fields.Integer(
        string=u'Cortesias: ',
        default=0,
    )
    contato = fields.Char(
        string=u'Contato: ',
    )
    nome_contato = fields.Char(
        string=u'Falar com: '
    )
    tipo_contato = fields.Selection(
        string=u'Tipo do Contato: ',
        selection=[
            ('empresario', u'Empresário'),
            ('artista', u'Artista'),
            ('agencia', u'Agência')
        ]
    )

    @api.onchange('apresentacao_ids')
    def _compute_cortesias(self):
        for artista in self:
            if artista.apresentacao_ids:
                artista.cortesias = artista.apresentacao_ids[-1].cortesias


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
