# -*- coding: utf-8 -*-
# Copyright 2017 Gabriel Cardoso de Faria
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Comunicação',
    'description': """
        Gerência de Comunicação""",
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Gabriel Cardoso de Faria',
    'depends': [
        'eventos',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/post.xml',
        'views/empresa.xml',
    ],
    'demo': [
    ],
}
