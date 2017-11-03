# -*- coding: utf-8 -*-
# Copyright 2017 Gabriel Cardoso de Faria
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class Post(models.Model):

    _name = 'post'
    _description = 'Postagem'

    name = fields.Char(
        string=u'Nome do Post: ',
    )
    tipo = fields.Selection(
        string=u'Tipo de publicação: ',
        selection=[
            ('festa', 'Festa'),
            ('outros', 'Outros'),
        ],
        default='festa',
    )
    pagina = fields.Selection(
        string=u'Página: ',
        selection=[
            ('barcultural', 'Bar Cultural'),
            ('dce', 'DCE'),
        ],
        default='barcultural',
    )
    
    state = fields.Selection(
        string=u'Situação',
        selection=[
            ('novo', u'Novo'),
            ('agendado', u'Agendado'),
            ('postado', u'Postado'),
            ('atrasado', u'Atrasado'),
            ('postado_atrasado', u'Postado em atraso'),
        ],
        default='novo',
    )
    
    festa_id = fields.Many2one(
        string=u'Festa',
        comodel_name='evento',
    )
    postar_em = fields.Datetime(
        string=u'Postar em: ',
    )
    postado_em = fields.Datetime(
        string=u'Postado em: ',
        store=True,
    )
    
    arte = fields.Binary(
        string=u'Arte',
    )
    texto = fields.Text(
        string=u'Texto do post',
    )
    
    responsavel_post = fields.Many2one(
        string=u'Responsavel por postar: ',
        comodel_name='responsavel',
    )
    responsavel_arte = fields.Many2one(
        string=u'Responsavel pela arte: ',
        comodel_name='responsavel',
    )
    responsavel_texto = fields.Many2one(
        string=u'Responsável pelo texto: ',
        comodel_name='responsavel',
    )

    terceirizada = fields.Boolean(
        string=u'Arte terceirizada?',
    )
    empresa = fields.Many2one(
        string=u'Empresa: ',
        comodel_name='empresa',
    )
    custo = fields.Float(
        string=u'Custo: ',
        digits=(16, 2),
    )
    
    @api.multi
    def agendar(self):
        self.state = 'agendado'
    
    @api.multi
    def postado(self):
        self.state = 'postado'
        self.postado_em = fields.Datetime.now()
    
    @api.multi
    def em_atraso(self):
        self.state = 'atrasado'
    
    @api.multi
    def post_atrasado(self):
        self.state = 'postado_atrasado'

