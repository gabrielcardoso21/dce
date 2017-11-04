# -*- coding: utf-8 -*-
# Copyright 2017 Gabriel Cardoso de Faria
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Divulgação',
    'description': """
        Gerência de Divulgação""",
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Gabriel Cardoso de Faria',
    'depends': [
        'eventos',
        'comunicacao',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/eventos_confirmados.xml',
    ],
    'demo': [
    ],
}
