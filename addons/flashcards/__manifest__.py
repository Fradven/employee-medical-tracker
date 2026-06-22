{
    'name': "Flashcards",
    'version': '17.0.1.0.0',
    'depends': ['base'],
    'author': "ldolne",
    'category': 'Website',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'views/flashcards_views.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'data/flashcards_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
}