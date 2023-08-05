import glob, os

import pandas as pd

import orms

def inject_all(df_class, *excludes):
    excludes = excludes or []
    for appname in filter(lambda name: not name.startswith('__'), dir(orms)):
        if appname in excludes:
            continue
        app = getattr(orms, appname)
        if callable(app):
            setattr(df_class, appname, app)

def inject_selective(df_class, *apps):
    for appname in filter(lambda name: not name.startswith('__'), dir(orms)):

        if appname in apps or appname.startswith('_'):
            app = getattr(orms, appname)
            if callable(app):
                setattr(df_class, appname, app)

def collectdf(path, **kwargs):
    path_list = glob.glob(path)
    dfs = []
    for p in path_list:
        fn, ext = os.path.splitext(p)
        if ext in ['.xls', '.xlsx']:
            df = pd.read_excel(p, **kwargs)
        elif ext in ['.csv']:
            df = pd.read_csv(p, **kwargs)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)
