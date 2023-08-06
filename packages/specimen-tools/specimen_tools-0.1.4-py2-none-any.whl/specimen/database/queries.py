# Copyright 2018 Jose Cambronero and Phillip Stanley-Marbell
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject
# to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import numpy as np
import pandas as pd
import sqlite3 as db

import dbtypes
from specimen import utils

def read_sql(sql, conn):
    # read sql with pandas but make sure column names are lowercase
    df = pd.read_sql(sql, conn)
    df.columns = df.columns.map(lambda x: x.lower())
    return df

class SpecimenQueries:
    """
    Contains helpful specimen database queries. Should be used as a starting point for analysis of specimen
    data.
    """

    def __init__(self, database_path=None):
        """
        Provides wrapper for queries. Caches queries where possible.

        :param database_path: Path to SQLITE database file
        """
        self.database_path = database_path
        self.conn = db.connect(database=self.database_path)
        # start use of foreign keys
        _cursor = self.conn.cursor()
        _cursor.execute('PRAGMA foreign_keys = ON')
        _cursor.close()
        self.cache = {}


    def _clear_cache(self):
        """ Clear cache, which stores prior query results """
        self.cache = {}


    def _drop_tables(self, tables):
        """
        Drop a set of tables from db (often used to materialize intermediate tables for ease of querying and
        then removing these to avoid affecting db state)

        :param tables: list of tables to drop
        :return: drops if they exist, ignores otherwise
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute('DROP TABLE ' + ','.join(map(str, tables)))
        except:
            pass
        finally:
            cursor.close()

    def _get_unknown_userid(self):
        """
        Retrieve user id associated with unknown user
        """
        cursor = self.conn.cursor()
        unknown_user_str = dbtypes.User.null
        cursor.execute("select id from users where uniqueid='%s'" % unknown_user_str)
        return cursor.fetchone()[0]


    def users_and_countries(self, use_cache=True):
        """
        Returns a table with userid and most likely country (based on carrier location frequency).

        :param use_cache: if true uses cached result, else clears database state and reruns query
        :return: pandas dataframe
        """
        key = 'user_and_countries'

        if use_cache and key in self.cache:
            return self.cache[key].copy()
        cursor = self.conn.cursor()

        if not use_cache:
            self._drop_tables(['user_country_freqs', 'user_and_likely_country'])

        # userid for unknown user
        unknown_user_id = self._get_unknown_userid()

        # can only return country info if userid is known
        cursor.execute(
            """
            CREATE TEMP TABLE user_country_freqs AS
            select userid, country, count(*) as ct
            from sessions where userid <> %d and country is not null
            group by userid, country
            """ % unknown_user_id
        )
        # assigns each user to country with most counts
        cursor.execute(
           """
          CREATE TEMP TABLE user_and_likely_country AS
          SELECT *
          FROM
          user_country_freqs JOIN (SELECT userid, max(ct) as max_ct FROM user_country_freqs GROUP BY userid) max_cts
          USING (userid)
          WHERE user_country_freqs.ct = max_cts.max_ct
          GROUP BY userid
          """
        )
        cursor.close()

        result = read_sql('SELECT * FROM user_and_likely_country', self.conn)
        self.cache[key] = result.copy()
        return result

    def create_reference_ids_table(self, vals, table_name='_ref'):
        """
        Create a temporary reference table by inserting values.
        This is used to speed up sqlite queries that are too slow when given
        the list directly in the query text (most likely a parsing issue?).
        """
        # remove existing
        self._drop_tables([table_name])
        cursor = self.conn.cursor()
        cursor.execute('CREATE TEMP TABLE %s (id INTEGER)' % table_name)
        for i, v in enumerate(vals):
            cursor.execute('INSERT INTO %s VALUES(%d)' % (table_name, v))


    def get_time_offset(self, event_ids, get_extra_info=True, use_cache=True):
        """
        Compute the time offset from the start of a session for a list of events.
        Only possible with data from JSON files. CSV files have dummy timestamps.

        :param event_ids: list of event ids to query
        """
        print "Warning: This is only valid for data from the json files! Timestamps in csv are dummies"
        if event_ids is None:
            raise ValueError('Must provide event ids ts')

        key = ('timestamps', tuple(event_ids), get_extra_info)
        if use_cache and key in self.cache:
            return self.cache[key].copy()

        # create event id references to query
        self.create_reference_ids_table(event_ids, table_name='_ref')

        ts_query =  """
        SELECT events.id as id, offsettimestamp, event FROM events, _ref
        WHERE events.id = _ref.id AND offsettimestamp >= 0
        """

        ts = read_sql(ts_query, self.conn)

        # adds additional information such as user id, and session id for matching up timestamps
        if get_extra_info:
            extra_info_query = """
            SELECT
                sessions.userid,
                events.id AS id,
                sessions.id AS sessionid
            FROM events, sessions, _ref
            WHERE events.id = _ref.id AND
            events.sessionid = sessions.id
            """
            extra_info_df = read_sql(extra_info_query, self.conn)
            ts = ts.merge(extra_info_df, how='left', on='id')

        self.cache[key] = ts.copy()
        return ts

    def get_devices(self, event_ids, use_cache=True):
        """
        Query the devices associated with particular event ids.
        :param event_ids: list of event ids to query
        """
        if event_ids is None:
            raise ValueError('Must provide event ids')

        # cast to tuple so that can be hashed
        key = ('devices', tuple(event_ids))
        if use_cache and key in self.cache:
            return self.cache[key].copy()

        # create event id references to query
        self.create_reference_ids_table(event_ids, table_name='_ref')

        devices_query = """
        select
        devices.name as device_name,
        events.id as eventid
        FROM
        sessions, events, devices, _ref
        WHERE
        events.id = _ref.id AND
        sessions.id = events.sessionid AND
        sessions.deviceid = devices.id
        """

        devices_df = read_sql(devices_query, self.conn)
        self.cache[key] = devices_df.copy()
        return devices_df

    def base_selections(self, min_turns=50, which='all', add_fields=None, use_cache=True):
        """
        Obtain base selections data, consisting of selections for known userids (i.e. this
        precludes data from the CSV files from Flurry, which do not have known user ids associated
        with each record). Selects only the first turn in a 'play',
        to control for game play. Selects data for users with at least `min_turns` such turns. Caches results

        :param min_turns: minimum number of first turns necessary for data, if 0, returns all
        :param which: one of 'all', 'correct', 'incorrect', determines what kind of selections are returned
        :param add_fields: add extra base fields from table selectionevents. If dict, uses keys as fields
        and values as names, if list uses elements as fields and names
        :param use_cache: if true, uses cached results, else clears database state and reruns.
        :return: pandas dataframe
        """
        if min_turns < 0:
            raise ValueError('min_turns must be > 0')
        if add_fields and not utils.is_iterable(add_fields):
            raise ValueError('add_fields must be iterable')
        if not which in ['all', 'correct', 'incorrect']:
            raise ValueError("which must be one of 'all', 'correct', 'incorrect'")

        key = ('first_sels', min_turns, which, add_fields)

        if use_cache:
            if key in self.cache:
                return self.cache[key].copy()
            else:
                # we may have created tables for different optional args (i.e. diff min_turns)
                self._drop_tables(['first_sels', 'enough_plays'])

        if not use_cache:
            self._drop_tables(['first_sels', 'enough_plays'])

        # cobble together additional fields from selectionevents
        added = ""
        if add_fields:
            if not isinstance(add_fields, dict):
                add_fields = dict(zip(add_fields, add_fields))
            added = ", " + (".".join(["%s as %s" % (f,n) for f, n in add_fields.iteritems()]))

        cursor = self.conn.cursor()

        # unknown user id
        unknown_user_id = self._get_unknown_userid()

        # filter to base data consisting of first-turns in play for known user ids
        print "Filtering down to first-turns in a play"
        cursor.execute("""
        -- compute the smallest eventid associated with each playid
        CREATE TEMP TABLE sel_cts AS
            SELECT MIN(eventid) as min_event_id
            FROM selectionevents
            where userid <> %d
            GROUP BY playid
        """ % unknown_user_id)

        print "Retrieving selection information for those turns"
        cursor.execute("""
        -- use this min eventid to select the first choice in each round
        CREATE TEMP TABLE first_sels AS
          SELECT
              userid, playid, id as selid, eventid,
              target_r, target_g, target_b,
              specimen_r, specimen_g, specimen_b,
              target_lab_l, target_lab_a, target_lab_b,
              specimen_lab_l, specimen_lab_a, specimen_lab_b,
              is_first_pick,
              target_h,
              target_s,
              target_v,
              specimen_h,
              correct
              %s
          FROM
            selectionevents
            INNER JOIN sel_cts
            ON selectionevents.eventid = sel_cts.min_event_id
          WHERE userid <> %d
        """  % (added, unknown_user_id)
        )

        # restrict to subset of users with at least min_turns
        if min_turns:
            cursor.execute(
                """
                CREATE TEMP TABLE enough_plays as
                SELECT userid FROM first_sels GROUP BY userid HAVING count(*) >= %s
                """ % min_turns
            )
            cursor.execute('DELETE FROM first_sels WHERE NOT userid IN (SELECT userid FROM enough_plays)')

        cursor.close()

        # filter to type of selections requested
        if which == 'all':
            results = read_sql('SELECT * FROM first_sels', self.conn)
        elif which == 'correct':
            results = read_sql('SELECT * FROM first_sels WHERE correct', self.conn)
        else:
            results = read_sql('SELECT * FROM first_sels WHERE NOT correct', self.conn)

        self.cache[key] = results.copy()

        return results

    def execute_adhoc(self, query, use_cache=True):
        """
        Execute ad-hoc queries over the Specimen database.

        :param query: String SQL query
        """
        key = query
        if use_cache and key in self.cache:
            return self.cache[key].copy()

        results = read_sql(query, self.conn)
        self.cache[key] = results.copy()
        return results

