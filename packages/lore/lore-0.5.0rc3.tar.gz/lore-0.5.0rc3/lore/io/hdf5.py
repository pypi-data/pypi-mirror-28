import pandas
import hashlib
import logging
import os

from abc import abstractmethod, abstractproperty

import lore.env
from lore.util import timer, timed

logger = logging.getLogger(__name__)


class Table(object):

    def __init__(self, connection, sql, params, chunksize):
        self.connection = connection
        self.sql = sql
        self.params = params
        self.chunksize = chunksize
        self.key = 'sql_' + self.orientation + hashlib.sha1(sql.encode('utf-8') + str(params).encode('utf-8')).hexdigest()
        self.key_columns = self.key + '_columns'
        self.key_min_itemsize = self.key + '_min_itemsize'
        self.loaded = False
        self._store = None
        self._min_itemsize = None
        self._columns = None

    @abstractmethod
    def __len__(self):
        pass

    @property
    def columns(self):
        if not self.loaded:
            self.load()
    
        if self._columns is None:
            with self.store as store:
                self._columns = list(store[self.key_columns])
    
        return self._columns

    @property
    def min_itemsize(self):
        if not self.loaded:
            self.load()
    
        if self._min_itemsize is None:
            with self.store as store:
                self._min_itemsize = store[self.key_min_itemsize].to_dict()
    
        return self._min_itemsize

    @property
    def store(self):
        if self._store is None:
            self._store = pandas.HDFStore(os.path.join(lore.env.data_dir, self.connection.name + '.h5'), complevel=7,
                                          complib='blosc')
    
        if not self._store.is_open:
            self._store.open()
    
        return self._store

    def select(self, columns=None):
        if not self._store.is_open:
            self._store.open()
        return self._store.select(self.key, columns=columns, chunksize=self.chunksize)
        
    @abstractproperty
    def orientation(self):
        return None
    
    @abstractmethod
    def load(self):
        pass
    
    @abstractmethod
    def index(self, columns, optlevel=7, kind='full'):
        pass


class Rows(Table):
    """ Row oriented table in chunks """
    def __getitem__(self, name):
        with self.store as store:
            return store.select(self.key, columns=name, chunksize=self.chunksize)

    def __len__(self):
        with self.store as store:
            return store.get_storer(self.key).nrows

    @property
    def orientation(self):
        return 'row'
    
    @timed(logging.INFO)
    def load(self):
        self.loaded = True
        
        with self.store as store:
            if self.key in store:
                return
        
        self._min_itemsize = {}
        for dataframe in pandas.read_sql(self.sql, self.connection._connection, chunksize=self.chunksize,
                                         params=self.params):
            logger.info('appending %i rows to hdf5' % len(dataframe))
            self._columns = dataframe.columns
            
            with self.store as store:
                resize = False
                for column in dataframe.columns:
                    series = dataframe[column]
                    if series.dtype == 'object':
                        # resize string columns on disk if required
                        max = int(series.str.encode('utf-8').str.len().max())
                        if column not in self._min_itemsize:
                            self.min_itemsize[column] = max
                        
                        if max > self._min_itemsize[column]:
                            self.min_itemsize[column] = max
                            resize = True
                
                if resize:
                    with timer('resize %s' % str(self.min_itemsize), logging.INFO):
                        temp = 'resize_' + self.key
                        store.get_node(self.key)._f_rename(temp)
                        
                        for chunk in store.select(temp, chunksize=self.chunksize):
                            store.append(self.key, chunk, index=False, min_itemsize=self.min_itemsize)
                        del store[temp]
                
                store.append(self.key, dataframe, index=False)
        
        with self.store as store:
            store[self.key_columns] = pandas.Series(self.columns)
            store[self.key_min_itemsize] = pandas.Series(self.min_itemsize)
    
    def index(self, columns, optlevel=7, kind='full'):
        self.store.create_table_index(self.key, columns=columns, optlevel=optlevel, kind=kind)


class Columns(Table):
    """ Column oriented table in chunks """

    def __getitem__(self, name):
        with self.store as store:
            return store.select(self.column_key(name), chunksize=self.chunksize)

    def __len__(self):
        with self.store as store:
            return store.get_storer(self.column_key(self.columns[0])).nrows

    @property
    def orientation(self):
        return 'column'

    @timed(logging.INFO)
    def load(self):
        self.loaded = True

        with self.store as store:
            if self.key in store:
                return
    
        self._min_itemsize = {}
        for dataframe in pandas.read_sql(self.sql, self.connection._connection, chunksize=self.chunksize, params=self.params):
            logger.info('appending %i rows to hdf5' % len(dataframe))
            self._columns = dataframe.columns

            with self.store as store:
                for column in dataframe.columns:
                    name = self.column_key(column)
                    series = dataframe[column]

                    if name.lower() == 'index':
                        raise AttributeError("'index' is a reserved word and cannot be used for a column name")

                    if series.dtype == 'object':
                        # resize string columns on disk if required
                        max = int(series.str.encode('utf-8').str.len().max())
                        if column not in self._min_itemsize:
                            self._min_itemsize[column] = max
                
                        if max > self._min_itemsize[column]:
                            self._min_itemsize[column] = max
                            min_itemsize = {column: max}

                            with timer('resize %s' % str(min_itemsize), logging.INFO):
                                temp = 'resize_' + name
                                store.get_node(name)._f_rename(temp)
                                
                                for chunk in store.select(temp, chunksize=self.chunksize):
                                    store.append(name, chunk, index=False, min_itemsize=min_itemsize)
                                del store[temp]

                    store.append(name, series, index=False)

        with self.store as store:
            store[self.key_columns] = pandas.Series(self.columns)
            store[self.key_min_itemsize] = pandas.Series(self.min_itemsize)

    def column_key(self, column):
        return self.key + '_' + str(column)
    
    def index(self, columns, optlevel=7, kind='full'):
        for column in columns:
            self.store.create_table_index(self.column_key(column), columns=column, optlevel=optlevel, kind=kind)


