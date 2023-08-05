from distutils.core import setup, Extension

dallar_subsidy_module = Extension('dallar_subsidy', sources = ['dallar_subsidy.cpp'])

setup (name = 'dallar_subsidy',
    version = '1.3',
    description = 'Subsidy function for Dallar',
    maintainer = 'Allar',
    maintainer_email = 'allar@gamemak.in',
    url = 'https://github.com/dallar-project/dallar-subsidy-python',
    keywords = ['dallar', 'dal', 'throestl'],
    ext_modules = [dallar_subsidy_module])
