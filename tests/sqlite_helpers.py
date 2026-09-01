from peers import sqlite3


def json_text_installed():
    return sqlite3.sqlite_version_info >= (3, 38, 0)

def jsonb_installed():
    return sqlite3.sqlite_version_info >= (3, 45, 0)


def compile_option(p):
    if not hasattr(compile_option, '_pragma_cache'):
        conn = sqlite3.connect(':memory:')
        curs = conn.execute('pragma compile_options')
        opts = [opt.lower().split('=')[0].strip() for opt, in curs.fetchall()]
        compile_option._pragma_cache = set(opts)
    return p in compile_option._pragma_cache
