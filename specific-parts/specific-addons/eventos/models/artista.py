# -*- coding: utf-8 -*-
# Copyright 2017 Gabriel Cardoso de Faria
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


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
    nome_completo = fields.Char(
        string=u'Nome Completo: ',
    )
    cpf = fields.Char(
        string=u'CPF: ',
    )
    rg = fields.Char(
        string=u'RG: ',
    )
    cep = fields.Char(
        string=u'CEP: ',
    )
    endereco = fields.Char(
        string=u'Endereço: ',
    )
    bairro = fields.Char(
        string=u'Bairro',
    )
    tipo = fields.Selection(
        string=u'Tipo de músico: ',
        selection=[
            ('banda', u'Banda'),
            ('dj', u'DJ'),
        ]
    )
    sexo = fields.Selection(
        string=u'Sexo: ',
        selection=[
            ('o', 'Masculino'),
            ('a', 'Feminino'),
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
