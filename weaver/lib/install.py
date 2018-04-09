from __future__ import absolute_import
from __future__ import print_function

import os

from weaver.engines import choose_engine
from weaver.lib.defaults import DATA_DIR
from weaver.lib.scripts import SCRIPT_LIST
from weaver.lib.tools import name_matches


def _install(args, use_cache, debug, compile):
    """Install scripts for weaver."""
    engine = choose_engine(args)
    engine.use_cache = use_cache

    script_list = SCRIPT_LIST(force_compile=True)
    scripts = name_matches(script_list, args['dataset'])
    if scripts:
        for script in scripts:
            print("=> Installing", script.name)
            try:
                script.download(engine, debug=debug)
                script.engine.final_cleanup()
            except Exception as e:
                print(e)
                if debug:
                    raise
    else:
        message = "The dataset \"{}\" isn't available in the Retriever. " \
                  "Run weaver.datasets()to list the currently available " \
                  "datasets".format(args['dataset'])
        raise ValueError(message)


def install_postgres(dataset, user='postgres', password='',
                     host='localhost', port=5432, database='postgres',
                     database_name=None, table_name=None,
                     compile=False, debug=False, quiet=False, use_cache=True):
    """Install scripts in postgres."""
    if not table_name:
        table_name = '{db}.{table}'
    if not database_name:
        database_name = '{db}'

    args = {
        'command': 'install',
        'database': database,
        'database_name': database_name,
        'engine': 'postgres',
        'dataset': dataset,
        'debug': debug,
        'host': host,
        'port': port,
        'password': password,
        'quiet': quiet,
        'table_name': table_name,
        'user': user,
        'use_cache': use_cache
    }

    _install(args, use_cache, debug, compile)


def install_sqlite(dataset, file=None, table_name=None,
                   compile=False, debug=False, quiet=False, use_cache=True):
    """Install scripts in sqlite."""
    if not table_name:
        table_name = '{db}_table'
    if not file:
        file = os.path.join(DATA_DIR, 'sqlite.db')

    args = {
        'command': 'install',
        'dataset': dataset,
        'engine': 'sqlite',
        'file': file,
        'quiet': quiet,
        'table_name': table_name,
        'use_cache': use_cache
    }

    _install(args, use_cache, debug, compile)



