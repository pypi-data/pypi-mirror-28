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
import psycopg2 as db

import dbtypes
from specimen import utils


class SpecimenQueries:
    """
    Contains helpful specimen database queries. Should be used as a starting point for analysis of specimen
    data.
    """
    DB_NAME = "specimen"

    def __init__(self, database_name=None):
        """
        Provides wrapper for queries. Caches queries where possible.

        :param database_name: Name of postgres database
        """
        database_name = SpecimenQueries.DB_NAME if database_name is None else database_name
        self.conn = db.connect(database=database_name)
        self.conn.autocommit = True
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
            select userid, country, count(*)
            from sessions where userid <> %d and country is not null
            group by userid, country;
            """ % unknown_user_id
        )
        # assigns each user to country with most counts
        cursor.execute(
           """
          CREATE TEMP TABLE user_and_likely_country AS
          SELECT DISTINCT ON (userid)  *
          FROM
          user_country_freqs JOIN (SELECT userid, max(count) FROM user_country_freqs GROUP BY userid) max_cts
          USING (userid)
          WHERE user_country_freqs.count = max_cts.max
          ORDER BY userid;
          """
        )
        cursor.close()

        result = pd.read_sql_query('SELECT * FROM user_and_likely_country', self.conn)
        self.cache[key] = result.copy()
        return result


    def get_time_offset(self, event_ids, get_extra_info=True, use_cache=True):
        """
        Compute the time offset from the start of a session for a list of events.
        Only possible with data from JSON files. CSV files have dummy timestamps.

        :param event_ids: list of event ids to query
        """
        print "Warning: This is only valid for data from the json files! Timestamps in csv are dummies"
        if event_ids is None:
            raise ValueError('Must provide event ids ts')

        if not isinstance(event_ids, str):
            # if not a string, we assume we got an iterable with actual ids
            event_ids = utils.to_csv_str(event_ids)

        key = ('timestamps', event_ids)
        if use_cache and key in self.cache:
            return self.cache[key].copy()

        ts_query =  """
        SELECT id, offsettimestamp, event FROM events
        WHERE id IN (%s) AND offsettimestamp >= 0
        """

        ts = pd.read_sql_query(ts_query % event_ids, self.conn)

        # adds additional information such as user id, and session id for matching up timestamps
        if get_extra_info:
            extra_info_query = """
            SELECT sessions.userid, events.id AS id, sessions.id AS sessionid
            FROM events, sessions
            WHERE events.sessionid = sessions.id AND events.id IN (%s)
            """
            extra_info_df = pd.read_sql_query(extra_info_query % event_ids, self.conn)
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
        if not isinstance(event_ids, str):
            event_ids = utils.to_csv_str(event_ids)

        key = ('devices', event_ids)
        if use_cache and key in self.cache:
            return self.cache[key].copy()

        devices_query = """
        select
        devices.name as device_name,
        events.id as eventid
        FROM
        sessions, events, devices
        WHERE
        events.id in (%s) AND
        sessions.id = events.sessionid AND
        sessions.deviceid = devices.id
        """ % event_ids

        devices_df = pd.read_sql_query(devices_query, self.conn)
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
        cursor.execute("""
        CREATE TEMP TABLE first_sels AS
        SELECT * FROM
            (SELECT userid, playid, id as selid, eventid,
            target_r, target_g, target_b,
            specimen_r, specimen_g, specimen_b,
            target_lab_l, target_lab_a, target_lab_b,
            specimen_lab_l, specimen_lab_a, specimen_lab_b,
            SUM(CASE WHEN id >=0 THEN 1 else 0 END) OVER (PARTITION BY playid ORDER BY eventid) as sel_ct,
            is_first_pick,
            target_h,
            target_s,
            target_v,
            specimen_h,
            correct
            %s
            FROM
            selectionevents
            WHERE userid <> %d) d
        WHERE sel_ct = 1
        """ % (added, unknown_user_id))

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
            results = pd.read_sql_query('SELECT * FROM first_sels', self.conn)
        elif which == 'correct':
            results = pd.read_sql_query('SELECT * FROM first_sels WHERE correct', self.conn)
        else:
            results = pd.read_sql_query('SELECT * FROM first_sels WHERE NOT correct', self.conn)

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

        results = pd.read_sql_query(query, self.conn)
        self.cache[key] = results.copy()
        return results

