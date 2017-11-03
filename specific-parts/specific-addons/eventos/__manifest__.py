# -*- coding: utf-8 -*-
# Copyright 2017 Gabriel Cardoso de Faria
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Eventos',
    'description': """
        Gerência de Eventos""",
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Gabriel Cardoso de Faria',
    'depends': [
        'report_py3o',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        
        'report/report_atracao.xml',

        'data/artista.csv',
        'data/responsavel.csv',
        'data/evento.csv',
        'data/atracao.csv',
        
        'views/evento.xml',
        'views/atracao.xml',
        'views/artista.xml',
        'views/responsavel.xml',
    ],
    'demo': [
    ],
}
