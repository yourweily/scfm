'''
Created on Aug 22, 2014

@author: Wei Li
@email: weily.li@gmail.com
'''
try:
    from cx_Freeze import setup, Executable
    import sys
    import pf
except ImportError:
    print("Error: no cx_Freeze module")




config = {
    'name':'structured cashflow model',
    'version': '0.1',
    'description': 'strucuted cash flow model',
    'author': 'Wei Li',
    'author_email': 'weily.li@gmail.com',
    'scripts': [],
    'executables':[Executable("view/main_ui.py")],
}

setup(**config)