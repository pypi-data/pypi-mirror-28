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
import sys

import psycopg2 as dbms


class Record(object):
    """
    Abstract class that all database tuples should extend. The expectation is that
    each table has its own class of tuples associated with it.
    """
    __metaclass__ = ABCMeta
    @property
    @abstractmethod
    def table(self):
        """ table associated with a given record type """
        pass

    @abstractmethod
    def insertionString(self, cursor):
        """ Define what a tuple for insertion should look like """
        pass

    @abstractmethod
    def schema(self):
        """ Define schema for that type of record """
        pass

    @abstractmethod
    def canFail(self):
        """ If true, bulk insertions are not performed to allow db to fail on a single insert """
        pass

    @abstractmethod
    def init(self):
        # should also be static but @staticmethod doesn't combine with @abstractmethod in older python versions
        pass


class ForeignKeyResolver:
    """
    Resolve foreign key references by using cached values or looking up in the database
    """
    @staticmethod
    def resolve(cursor, tbl, col, op, target, cache):
        """ Resolve references """
        # check cache again, just in case it has arrived in the meantime
        ref = cache[target] if target in cache else None
        # if not, fetch from db
        if not ref:
            if target:
                payload = "select id from %s where %s %s %s" % (tbl, col, op, target)
            else:
                # perform a check for NULL, if target is none
                payload = "select id from %s where %s IS NULL" % (tbl, col)
            try:
                cursor.execute(payload)
                ref = cursor.fetchone()[0]
            except Exception:
                print "Reference lookup error on %s" % payload
            cache[target] = ref
        return ref

    @staticmethod
    def lookup(target, cache):
        return cache[target] if target in cache else None


class User(Record):
    """ Specimen game user """
    cache = {}
    table =  "Users"
    enumTypes = "CREATE TYPE GenderEnum as ENUM ('male', 'female')"
    charLimit = 40
    schema = "(id SERIAL PRIMARY KEY, uniqueId CHAR(%s) UNIQUE, birthYear INTEGER, gender GenderEnum)" % charLimit
    canFail = True
    # stub for data that is not associated with any user, gets assigned to this Unknown user
    null = "Unknown"

    def __init__(self, uniqueId, birthYear, gender):
        # missing replaced with null
        self.uniqueId = User.null if not uniqueId else uniqueId
        self.birthYear = birthYear
        self.gender = gender.lower() if gender and gender.lower() in ['male', 'female'] else None

    def insertionString(self, cursor):
        payload = "(default, '%s', %s, '%s')" % (self.uniqueId, self.birthYear, self.gender)
        return str(payload)

    @staticmethod
    def resolveRef(cursor, target):
        target = "'%s'" % target if target else None
        return ForeignKeyResolver.resolve(cursor, User.table, "uniqueId", "=", target, User.cache)

    @staticmethod
    def lookupRef(target):
        return ForeignKeyResolver.lookup(target, User.cache)

    @staticmethod
    def init():
        return User(User.null, None, None)


class Device(Record):
    """ Device on which user played Specimen game """
    # from name to id
    cache = {}
    table = "Devices"
    charLimit = 100
    schema = "(id SERIAL PRIMARY KEY, name VARCHAR(%s) UNIQUE)" % charLimit
    canFail = True
    null = "Unknown"

    def __init__(self, deviceName):
        # truncate if longer than limit
        self.deviceName = Device.sanitize(deviceName)

    def insertionString(self, cursor):
        return "(default, '%s')" % self.deviceName

    @staticmethod
    def resolveRef(cursor, target):
        target = "'%s'" % target if target else None
        return ForeignKeyResolver.resolve(cursor, Device.table, "name", "=", target, Device.cache)

    @staticmethod
    def lookupRef(target):
        return ForeignKeyResolver.lookup(target, Device.cache)

    @staticmethod
    def init():
        return Device(Device.null)

    @staticmethod
    def sanitize(name):
        return Device.null if not name else name[ :Device.charLimit]


class Carrier(Record):
    """ Service provider (carrier) for Specimen game user's device """
    # from name to id
    cache = {}
    table = "Carriers"
    charLimit = 100
    schema = "(id SERIAL PRIMARY KEY, name VARCHAR(%s) UNIQUE)" % charLimit
    canFail = True
    null = "Unknown"

    def __init__(self, carrierName):
        # truncate if longer than limit
        self.carrierName = Carrier.sanitize(carrierName)

    def insertionString(self, cursor):
        return "(default, '%s')" % self.carrierName

    @staticmethod
    def resolveRef(cursor, target):
        target = "'%s'" % target if target else None
        return ForeignKeyResolver.resolve(cursor, Carrier.table, "name", "=", target, Carrier.cache)

    @staticmethod
    def lookupRef(target):
        return ForeignKeyResolver.lookup(target, Carrier.cache)

    @staticmethod
    def init():
        return Carrier(Carrier.null)

    @staticmethod
    def sanitize(name):
       return Carrier.null if not name else name[ :Carrier.charLimit]


class Session(Record):
    """ A game session, defined as the time from an instance start to the instance end """
    table = "Sessions"
    schema = """
        (
        id INTEGER PRIMARY KEY,
        userId INTEGER REFERENCES Users(id) ON DELETE CASCADE,
        startTimestamp BIGINT, sessionLength BIGINT,
        version SMALLINT, country CHAR(2),
        carrierId INTEGER REFERENCES Carriers(id), deviceId INTEGER REFERENCES Devices(id),
        longitude REAL, latitude REAL
        )
        """
    canFail = True
    indices = [("sessions_userid_idx", "sessions(userid)")]

    def __init__(self, sessionId, uniqueId, startTimestamp, sessionLength, version, country, carrierName, deviceName, lon, lat):
        self.sessionId = sessionId
        self.uniqueId = uniqueId
        self.userId = User.lookupRef(uniqueId)
        self.startTimestamp = startTimestamp
        self.sessionLength = sessionLength
        self.version = version
        self.country = country if country and country.lower() != "unknown" else None
        self.carrierName = Carrier.sanitize(carrierName)
        self.deviceName = Device.sanitize(deviceName)
        self.carrierId = Carrier.lookupRef(carrierName)
        self.deviceId = Device.lookupRef(deviceName)
        self.lon = lon
        self.lat = lat

    def getForeignKeys(self, cursor):
        if not self.carrierId:
            self.carrierId = Carrier.resolveRef(cursor, self.carrierName)

        if not self.deviceId:
            self.deviceId = Device.resolveRef(cursor, self.deviceName)

        if not self.userId:
            self.userId = User.resolveRef(cursor, self.uniqueId)

    def insertionString(self, cursor):
        self.getForeignKeys(cursor)
        payload = "(%s, %s, %s, %s, %s, '%s', %s, %s, %s, %s)" % (
            self.sessionId,
            self.userId,
            self.startTimestamp,
            self.sessionLength,
            self.version,
            self.country,
            self.carrierId,
            self.deviceId,
            self.lon,
            self.lat,
        )
        return str(payload)

    @staticmethod
    def init():
        return None


class Event(Record):
    """ An event in a Specimen game, defined as actions such as game start/end, specimen selection etc. """
    table = "Events"
    enumTypes = """
        CREATE TYPE EventType as
        ENUM
        (
        'start game', 'select specimen', 'lose level', 'replay level',
        'purchase activity', 'win level', 'spectrum cleared', 'share press'
        )
        """
    schema = """(
        id INTEGER PRIMARY KEY,
        sessionId INTEGER REFERENCES Sessions(id) on DELETE CASCADE,
        offsetTimestamp BIGINT, event EventType)
        """
    canFail = False
    indices = [("events_sessionid_idx", "events(sessionid)")]

    def __init__(self, eventId, sessionId, offsetTimestamp, event):
        self.eventId = eventId
        self.sessionId = sessionId
        self.offsetTimestamp = offsetTimestamp
        self.event = event

    def insertionString(self, cursor):
        payload ="(%s, %s, %s, '%s')" % (self.eventId, self.sessionId, self.offsetTimestamp, self.event,)
        return str(payload)

    @staticmethod
    def init():
        return None


class SelectionEvent(Record):
    """ Event triggered when a player selects a specimen """
    table = "SelectionEvents"
    schema =  """
        (
        id SERIAL PRIMARY KEY,
        userId INTEGER REFERENCES Users(id) ON DELETE CASCADE,
        eventId INTEGER REFERENCES Events(id) ON DELETE CASCADE,
        playId INTEGER,
        specimen_r DOUBLE PRECISION, specimen_g DOUBLE PRECISION, specimen_b DOUBLE PRECISION,
        target_r DOUBLE PRECISION, target_g DOUBLE PRECISION, target_b DOUBLE PRECISION,
        specimen_h DOUBLE PRECISION, specimen_s DOUBLE PRECISION, specimen_v DOUBLE PRECISION,
        target_h DOUBLE PRECISION, target_s DOUBLE PRECISION, target_v DOUBLE PRECISION,
        specimen_lab_l DOUBLE PRECISION, specimen_lab_a DOUBLE PRECISION, specimen_lab_b DOUBLE PRECISION,
        target_lab_l DOUBLE PRECISION, target_lab_a DOUBLE PRECISION, target_lab_b DOUBLE PRECISION,
        correct BOOLEAN, pos_x DOUBLE PRECISION, pos_y DOUBLE PRECISION, is_first_pick BOOLEAN
        )
    """
    canFail = False
    indices = [
        ("selectionevents_userid_idx", "selectionevents(userid)"),
        ("selectionevents_eventid_idx", "selectionevents(eventid)"),
        ("selectionevents_playid_idx", "selectionevents(playid)")
    ]

    def __init__(
            self,
            eventId,
            uniqueId,
            playId,
            specimen_rgb,
            target_rgb,
            specimen_hsv,
            target_hsv,
            specimen_lab,
            target_lab,
            correct,
            pos_x,
            pos_y,
            is_first_pick
    ):
        self.uniqueId = uniqueId
        self.userId = User.lookupRef(uniqueId)
        self.eventId = eventId
        self.playId = playId
        (self.specimen_r, self.specimen_g, self.specimen_b) = specimen_rgb
        (self.target_r, self.target_g, self.target_b) = target_rgb
        (self.specimen_h, self.specimen_s, self.specimen_v) = specimen_hsv
        (self.target_h, self.target_s, self.target_v) = target_hsv
        (self.specimen_lab_l, self.specimen_lab_a, self.specimen_lab_b) = specimen_lab
        (self.target_lab_l, self.target_lab_a, self.target_lab_b) = target_lab
        self.correct = correct
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.is_first_pick = is_first_pick

    def getForeignKeys(self, cursor):
        if not self.userId:
            self.userId = User.resolveRef(cursor, self.uniqueId)

    def insertionString(self, cursor):
        self.getForeignKeys(cursor)
        payload = "(default, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (
            self.userId,
            self.eventId,
            self.playId,
            self.specimen_r,
            self.specimen_g,
            self.specimen_b,
            self.target_r,
            self.target_g,
            self.target_b,
            self.specimen_h,
            self.specimen_s,
            self.specimen_v,
            self.target_h,
            self.target_s,
            self.target_v,
            self.specimen_lab_l,
            self.specimen_lab_a,
            self.specimen_lab_b,
            self.target_lab_l,
            self.target_lab_a,
            self.target_lab_b,
            self.correct,
            self.pos_x,
            self.pos_y,
            self.is_first_pick,
        )
        return str(payload)

    @staticmethod
    def init():
        return None


class PurchaseEvent(Record):
    """ Event triggered when the user buys an item inside the Specimen game """
    table = "PurchaseEvents"
    schema = """(
        id SERIAL PRIMARY KEY,
        eventId INTEGER REFERENCES Events(id) ON DELETE CASCADE,
        cost INTEGER,
        itemPurchased VARCHAR(40)
        )"""
    canFail = False
    indices = [("purchaseevents_eventid_idx", "purchaseevents(eventid)")]

    def __init__(self, eventId, cost, itemPurchased):
        self.eventId = eventId
        self.cost = cost
        self.itemPurchased = itemPurchased

    def insertionString(self, cursor):
        payload ="(default, %s, %s, '%s')" % (self.eventId, self.cost, self.itemPurchased,)
        return str(payload)

    @staticmethod
    def init():
        return None


class LevelEvent(Record):
    """ Events related to different levels in Specimen """
    table = "LevelEvents"
    enumTypes = "CREATE TYPE SpectrumEnum AS ENUM ('alpha', 'beta', 'delta', 'epsilon', 'gamma', 'zeta')"
    schema = """
        (
        id SERIAL PRIMARY KEY,
        eventId INTEGER REFERENCES Events(id) ON DELETE CASCADE,
        spectrum SpectrumEnum, level SMALLINT,
        score BIGINT, boosterUsed BOOLEAN
        )
    """
    canFail = False
    indices = [("levelevents_eventid_idx", "levelevents(eventid)")]

    def __init__(self, eventId, spectrum, level, score, boosterUsed):
        self.eventId = eventId
        self.spectrum = spectrum
        self.level = level
        self.score = score
        self.boosterUsed = boosterUsed

    def insertionString(self, cursor):
        payload ="(default, %s, '%s', %s, %s, %s)" % (self.eventId, self.spectrum, self.level, self.score, self.boosterUsed,)
        return str(payload)

    @staticmethod
    def init():
        return None

