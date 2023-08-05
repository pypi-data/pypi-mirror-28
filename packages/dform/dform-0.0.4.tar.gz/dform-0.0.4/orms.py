import re
from collections import namedtuple

import numpy as np
import pandas as pd


not_op = '~'
isin_op = '{}'
regex_op = '$'
cmp_ops = ['<', '>', '=','==', '<=', '>=']
range_ops = ['[]', '[)', '(]', '()']


def _concat_ops(self, ops=[not_op,isin_op,regex_op,cmp_ops,range_ops]):
    ret = []
    for op in ops:
        if isinstance(op, str):
            op = [op]
        ret += op
    return ret


def _get_mask(self, colnm, op, val):
    nt = False
    s = self[colnm]
    if not_op in op:
        nt = True
        op = op.replace(not_op, '')

    if op in cmp_ops:
        if op == '<':
            mask = s < val
        elif op == '>':
            mask = s > val
        elif op == '>=':
            mask = s >= val
        elif op == '<=':
            mask = s <= val
        else:
            mask = s == val

    elif op == regex_op:
        mask = s.str.contains(val)
    elif op in range_ops:
        if len(val) < 2:
            raise ValueError(
                'Range operator {} needs 2 more than values but given {}'.format(op, val)
            )
        start, *_, end = sorted(val)
        if op == '[]':
            mask = (start <= s) & (s <= end) 
        elif op == '[)':
            mask = (start <= s) & (s < end)
        elif op == '(]':
            mask = (start < s) & (s <= end)
        else:
            mask = (start < s) & (s < end)
    elif op == isin_op:
        mask = s.isin(val)
    else:
        mask = s == val
    
    if nt:
        return ~mask 
    return mask


def _exp_parser(self, colexp):
    matched = list(filter(lambda x:x==colexp, self.columns))
    if len(matched) == 1:
        return '==', matched[0]
    fixed = list(filter(lambda x: x in colexp, self.columns))

    if len(fixed) == 0:
        raise ValueError('Column Expression Error: {}'.format(colexp))
    elif len(fixed) > 1:
        raise ValueError('Ambiguous, column name contains Operators?: {}'.foramt(fixed))
    else:
        colnm = fixed[0]
        op = colexp.replace(colnm, '')
        ntop = ''

        if not_op in op:
            op = op.replace(not_op, '') or '=='
            ntop = not_op
        if len(op) > 2:
            raise ValueError('Not Valid operator: {}'.format(op))
        else:
            if op in self._concat_ops():
                return ntop + op, colnm
            else:
                raise ValueError('Not Valid operator: {}'.format(op))


def _reduce_masks(self, masks, setop_exp):
    setops = '\|\^\&'
    optrex = re.compile(r'\||\&|\^')
    setop_exp = setop_exp.strip()

    if setop_exp in ['&', '^', '|']:
        mask, *rest = masks
        for m in rest:
            exec('mask{}=m'.format(setop_exp))
        return mask

    maskset = {m.name: m for m in masks}
    opts = optrex.findall(setop_exp)
    colnms = optrex.split(setop_exp)

    outofs = list(set(colnms) - maskset.keys())

    if outofs:
        raise ValueError('''InValid setop expression {}: 
            {} are not in column which states at where clause'''.format(setop_exp, outofs))

    if len(opts) + 1 != len(colnms):
        raise ValueError('InValid setop expression: {}'.format(setop_exp))

    mask = None

    for col in colnms:
        m = maskset[col]
        if mask is None:
            mask = m
        else:
            op = opts.pop(0)
            exec('mask{}=m'.format(op))
    return mask


def _get_indexer(self, where, setop='&'):
    if callable(where):
        mask = where(self)
    elif isinstance(where, dict):
        masks = []
        for colexp, app in where.items():
            if callable(app):
                if colexp in self.columns:
                    masks.append(app(self))
            else:
                op, colnm, = self._exp_parser(colexp)
                masks.append(self._get_mask(colnm, op, app))
        mask = self._reduce_masks(masks, setop)
    else:
        mask = self.index
    return mask


def select(self, *args, where=lambda df: df.index, setop='&'):
    '''Usage:
        df.select('name', 'age', 'gender', 
            where=lambda row: (row.gender == 'F')&(row.name.str.contains('L'))
        )
    '''
    if args == ('*',) or not args:
        args = self.columns
    indexer = self._get_indexer(where, setop)
    return self.loc[indexer, args]


def update(self, *args, set=lambda df: df, where=lambda df: df.index, **kwargs):
    '''Usage:
        df.update('name',
          set=lambda df: df.name.str.upper(),
          where=lambda df: df.age > 15
        )
    '''
    df = self.copy()
    indexer = self._get_indexer(where, **kwargs)
    
    if callable(set):
        df.loc[indexer, args] = set(df)
    elif isinstance(set, dict):
        for colnm, app in set.items():
            if colnm not in df.columns:
                continue
            df.loc[indexer, colnm] = app(df) if callable(app) else app
    else:
        df.loc[indexer, args] = set
    return df

def join(self, *args, **kwargs):
    return self.merge(*args, **kwargs)

def distinct(self, *args, **kwargs):
    '''Usage:
        df.distinct('location', 'gender')
    '''
    return self.drop_duplicates(args, **kwargs)

def annotate(self, **aggset):
    '''Usage:
        df.add_column(
            level=lambda df: np.where(df.age>15, 'high', 'low')
        )
    '''
    get_crit = lambda app: app(self) if callable(app) else app
    df = self.copy()
    for colnm, app in aggset.items():
        # df[colnm] = app(df) if callable(app) else app
        if callable(app):
            df[colnm] = app(df)
        elif isinstance(app, dict):
            for g, fset in app.items():
                if isinstance(fset, dict):
                    for tgt, f in fset.items():
                        df[colnm] = df.groupby(g)[tgt].transform(f)
                else:
                    # df[colnm] = getattr(df[g], fset)()
                    df[colnm] = df[g][fset]()
        elif isinstance(app, set):
            if app:
                df[colnm] = df[app.pop()]
        else:
            df[colnm] = app
    return df

def orderby(self, *columns):
    '''Usage:
        df.orderby('gender', '-age')
       Description: '-' prefix means order by descending
    '''
    ways = []
    cols = []
    
    for colnm in filter(None, columns):
        if colnm in self.columns:
            cols.append(colnm)
            ways.append(1)
        else:
            if colnm[0] == '-' and colnm[1:] in self.columns:
                cols.append(colnm[1:])
                ways.append(0)
    return self.sort_values(cols, ascending=ways)


def aggregate(self, **aggset):
    aggs = {}
    for retcol, app in aggset.items():
        for g, fset in app.items():
            if isinstance(fset, dict):
                df = self.groupby(g).agg(fset)
            else:
                df = self.groupby(g).agg(app)

        return df.rename(columns={list(fset)[0]:retcol})


def compare(self, other, pk, as_index=False):
    if isinstance(pk, str):
        pk = [pk]
    other = pd.DataFrame(other)

    df1 = self.copy()
    df2 = other.copy()
    
    for pkcol in pk:
        df1_hasnull = df1[pkcol].isnull().any()
        df2_hasnull = df2[pkcol].isnull().any()

        if any([df1_hasnull, df2_hasnull]):
            raise ValueError('pk has null value: {}'.format(pkcol))

    df1.set_index(pk, inplace=True)
    df2.set_index(pk, inplace=True)

    if not all([df1.index.is_unique, df2.index.is_unique]):
        raise ValueError('pk is not unique {}'.format(pk))

    df1.drop(columns=set(df1.columns)-set(df2.columns), inplace=True)
    df2.drop(columns=set(df2.columns)-set(df1.columns), inplace=True)

    mask_added = df2.index.difference(df1.index)
    mask_deleted = df1.index.difference(df2.index)
    mask_notchanged = df1.index.intersection(df2.index)

    df_added = df2.loc[mask_added]
    df_deleted = df1.loc[mask_deleted]
    df_notchanged = df1.loc[mask_notchanged]

    df1 = df1.loc[mask_notchanged]
    df2 = df2.loc[mask_notchanged]

    null_mask = df1.isnull() & df2.isnull()
    changed = (df1 != df2) | null_mask

    df_changed_from = df1[changed].dropna(how='all')
    df_changed_to = df2[changed].dropna(how='all')

    ch_from = df_changed_from.stack().dropna()
    ch_to = df_changed_to.stack().dropna()
    ch_info = pd.concat([ch_from, ch_to], axis=1, keys=['from', 'to'])
    ch_info.index.names = pk+['where']
    ch_info.reset_index(inplace=True)
    if as_index == True:
        ch_info.set_index(pk+['where'], inplace=True)
    
    nt = namedtuple('compare', 'added deleted changes')
    comp = nt(added=df_added, deleted=df_deleted, changes=ch_info)
    return comp


def top(self, column, ntop=1, ascending=False, **kwargs):
    rank_top = self[column].rank(**kwargs).min()
    rank_bottom = self[column].rank(**kwargs).max()

    if isinstance(ntop, float):
        if 0 < ntop < 1:
            if ascending == True:
                df = self.loc[self[column].rank()/self.shape[0] <= ntop]
                df = df.sort_values([column], ascending=ascending)
            else:
                df = self.loc[self[column].rank()/self.shape[0] >= 1 - ntop]
                df = df.sort_values([column], ascending=ascending)
        else:
            raise ValueError('If type of ntop is float, ntop might be 0 < ntop < 1')
    else:
        if ascending == True:
            df = self.loc[self[column].rank(**kwargs) <= ntop]
            df = df.sort_values([column], ascending=ascending)[:ntop]
            if df.shape[0] == 0:
                df = self.loc[self[column].rank()==rank_top][:ntop]
                df = df.sort_values([column], ascending=ascending)
        else:
            df = self.loc[self[column].rank(**kwargs) >= rank_bottom - ntop]
            df = df.sort_values([column], ascending=ascending)[:ntop]
            if df.shape[0] == 0:
                df = self.loc[self[column].rank() == rank_bottom][:ntop]
                df = df.sort_values([column], ascending=ascending)
    return df

def types(self, **typeset):
    '''Usage:
        df.types(age=int, gender=str)
    '''
    df = self.copy()
    for colnm, astype in typeset.items():
        df[colnm] = df[colnm].astype(astype)
    return df

def map(self, if_not_exists=None, **mappings):
    df = self.copy()
    for colnm, map in mappings.items():
        if colnm not in df.columns:
            continue
        maps = lambda val: map.get(val, if_not_exists or val)
        df[colnm] = df[colnm].map(maps)
    return df

def first(self):
    rows, cols = self.shape
    if rows > 0:
        return self.loc[0]

def last(self):
    rows, cols = self.shape
    if rows >0:
        return self.loc[rows-1]

def to_dictlist(self):
    '''returns list of dict as record
    '''
    return self.to_dict('record')

def to_tuplelist(self, header=False, columns=None, index=False, **kwargs):
    if columns:
        df = self.select(*columns)
    else:
        df = self
    records = list(df.to_records(index=index, **kwargs))

    if header == True:
        records = [tuple(df.columns)] + records
    return records

