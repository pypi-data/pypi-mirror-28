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


from abc import ABCMeta, abstractmethod
from collections import deque
import datetime
import sys

import psycopg2 as dbms

from queries import SpecimenQueries


class Database:
    """
    Simple database wrapper. Buffers writes to database. Takes record information and intializes tables
    if requested. Clears record-level key caches as necessary.
    """
    def __init__(self, name, recordTypes, bufferSize, cacheLimit):
        self.recordTypes = recordTypes
        self.buffer = deque()
        # flushes when size limit reached
        self.bufferSize = bufferSize
        # database must already exist
        self.conn = dbms.connect(database=name)
        # psycopg2 (and it seems postgres) don't support read uncommitted (which we need
        # to lookup reference values...)
        # TODO: fix this...having it on autocommit makes this not really great to use
        self.conn.autocommit = True
        self.cacheLimit = cacheLimit
        # object for specimen database queries (e.g. for unknown user id)
        self.specimen_queries = SpecimenQueries(database_name=name)

    def flush(self):
        """
        Flush buffer to database disk and clear local caches in each table
        :return:
        """
        # split writes by table
        print "[%s] Performing flush to database" % datetime.datetime.now()
        currentTable = None
        currentBatch = deque()
        while self.buffer:
            # collect sequence of writes associated with a given table
            while self.buffer and self.buffer[-1].table == currentTable:
                currentBatch.appendleft(self.buffer.pop())
            if currentBatch:
                self.__writeBatch(currentBatch)
                currentBatch.clear()
            # move on to next table in batch
            if self.buffer:
                currentTable = self.buffer[-1].table

    def clearCaches(self):
        """
        Clear local caches for each table's foreign key references. Called at each flush (so cache may actually grow
        beyond limit if the buffer size is too large).
        :return:
        """
        for recordType in self.recordTypes:
            try:
                if len(recordType.cache) >= self.cacheLimit:
                    recordType.cache.clear()
            except AttributeError:
                pass

    def __writeBatch(self, batch):
        """
        Write a batch of records for the same table to disk
        :param batch: collection of records for same table
        :return:
        """
        # insertionString needs cursor to make sure resolves any necessary foreign key references
        cursor = self.conn.cursor()
        recType = batch[0]
        tuples = [ record.insertionString(cursor) for record in batch ]
        # replace None in tuples with NULL
        clean_tuples = [ self.remove_None(tuple) for tuple in tuples ]
        # some record types may fail if they have integrity constraints
        if recType.canFail:
            for tuple in clean_tuples:
                try:
                    # tuples that may fail need to be written tuple at a time rather than in bulk
                    self.__write(cursor, recType.table, tuple)
                except dbms.IntegrityError:
                    # ok to fail for these, allows us to just try to insert
                    # for records with unique columns and offload error handling to dbms
                    pass
        else:
            # bulk values string
            joined = ", ".join(clean_tuples)
            try:
                self.__write(cursor, recType.table, joined)
            except dbms.DatabaseError as e:
                # if there was a database error we're better off just killing the process
                print e.message
                print joined
                sys.exit(1)
        cursor.close()

    def __write(self, cursor, table, msg):
        payload = "INSERT INTO " + table + " VALUES " + msg
        cursor.execute(payload)

    def remove_None(self, msg):
        """
        remove None from tuple string representation and replace with NULL (None comes from python)
        :param msg:
        """
        return msg.replace("'None'", "NULL").replace("None", "NULL")

    def insert(self, record):
        """
        Insert record into appropriate table. Lazy writing, flush if necessary.
        :param record: instance of Record class
        """
        if len(self.buffer) >= self.bufferSize:
            self.flush()
        # writes are done in order of insert
        self.buffer.appendleft(record)

    def insertMany(self, record_list):
        """
        wrapper around insert to deal with a list of records
        :param record_list:
        """
        for record in record_list:
            self.insert(record)

    def create_tables(self):
        """
        Initialize tables with defined schemas, necessary enumeration types, and dummy records where necessary. Note
        that this is done in the order of recordTypes, so any dependencies (e.g. foreign key references)
        should be reflected in the order.
        """
        cursor = self.conn.cursor()
        for recordType in self.recordTypes:
            table = recordType.table
            print "Creating table %s" % table
            # try to write any relevant enumeration datatypes
            try:
                cursor.execute(recordType.enumTypes)
            except AttributeError:
                # not all tables require enumeration types
                pass
            cursor.execute("CREATE TABLE %s %s" % (table, recordType.schema))
            if recordType.init():
                # some tables may need an initial record for stub values
                print "Inserting initial dummy record for %s" % table
                self.__writeBatch([recordType.init()])
        cursor.close()

    def create_indices(self):
        """
        After a large amount of data has been parsed and inserted, it may be useful to construct database
        indices
        """
        cursor = self.conn.cursor()
        for recordType in self.recordTypes:
            try:
                for (name, definition) in recordType.indices:
                    print "Creating index %s" % name
                    cursor.execute("CREATE INDEX %s ON %s" % (name, definition))
            except (AttributeError, dbms.ProgrammingError):
                # didn't have indices or already declared
                pass
        cursor.close()

    def drop_indices(self):
        """
        Before inserting a large amount of data, it may speed things up significantly to drop indices and
        rebuild afterwards
        """
        cursor = self.conn.cursor()
        for recordType in self.recordTypes:
            try:
                for (name, _) in recordType.indices:
                    print "Dropping index %s" % name
                    cursor.execute("DROP INDEX %s" % name)
            except (AttributeError, dbms.ProgrammingError):
                # didn't have indices or already declared
                pass
        cursor.close()

    def build_stats(self):
        """ Update the database statistics """
        print "Updating database statistics"
        cursor = self.conn.cursor()
        cursor.execute("ANALYZE")
        cursor.close()

    def remove_duplicate_sessions(self):
        """ 
        Remove duplicate sessions (and other relevant records by cascading).
        This is run after inserting records and assumes data has been populated into the db.
        If it is run on an empty database, it will likely fail (or produce incorrect effects).
        
        """
        print "Removing duplicate sessions and related records"
        unknown_user_id = self.specimen_queries._get_unknown_userid()
        
        rm_query = """
        CREATE TEMP TABLE duplicated_sessions AS
        SELECT id FROM
        (
            SELECT id,
            SUM(CASE WHEN TRUE THEN 1 else 0 END) OVER
            (PARTITION BY starttimestamp, sessionlength, userid, country ORDER BY id) as iter
            FROM
            sessions INNER JOIN
            (
                SELECT
                starttimestamp, sessionlength, userid, country
                FROM sessions
                WHERE userid <> %d
                GROUP BY starttimestamp, sessionlength, userid, country HAVING count(*) > 1
            ) repeated -- find sessions that are repeated
            USING (starttimestamp, sessionlength, userid, country)
            WHERE sessions.userid <> %d
        ) ordered_repeated -- order sessions, so that we delete anything that is not the first occurrence
        WHERE iter > 1;
        -- perform actual deletion, related records are deleted by cascading deletes
        DELETE FROM sessions WHERE id in (SELECT id from duplicated_sessions);
        """ % (unknown_user_id, unknown_user_id)
        cursor = self.conn.cursor()
        cursor.execute(rm_query)
        cursor.close()

    def clear(self):
        """ Clear internal state information """
        self.buffer.clear()
        self.clearCaches()

