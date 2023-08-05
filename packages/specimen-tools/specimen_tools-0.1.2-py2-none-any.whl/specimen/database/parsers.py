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


from collections import defaultdict
import csv
from datetime import datetime
import json

import colorsys
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color

from dbtypes import *
from specimen import utils


class AbstractSpecimenParser(object):
    """
    Base class to extend for all specimen data parsers.
    """
    def __init__(self, db):
        """
        :param db: database object (from specimen_database). The database must already exist
        as the parser needs to query it to obtain a couple of key identifiers.
        """
        self.db = db
        # get some important values from database
        self.get_state_info()

    def get_next_id(self, tbl, col="id"):
        """
        Get the next (largest) availble id in a sequence of unique identifiers (queries database to get value)
        :param tbl:
        :return:
        """
        cursor = self.db.conn.cursor()
        cursor.execute("select max(%s) from %s" % (col, tbl))
        v = cursor.fetchone()
        cursor.close()
        if not v[0]:
            # hadn't initiated the sequence
            return 1
        else:
            return v[0] + 1

    def get_state_info(self):
        """
        Obtains some important state information necessary for every new file to be parsed
        :return:
        """
        self.session_id = self.get_next_id("sessions")
        self.event_id = self.get_next_id("events")
        self.play_id = self.get_next_id("selectionevents", col="playid")
        print "Updated parser state. session id: %s, event id: %s, play id: %s" % (self.session_id, self.event_id, self.play_id)
        # keep track of these in case we need to delete data
        self.start_session_id = self.session_id
        self.start_event_id = self.event_id
        # keep around some target color information to flag selections as first in their streak
        self.prev_target_color = None

    def is_missing(self, s):
        """
        Check if a string is missing, this includes None, zero length and NA strings
        :param s: string to check if missing
        :return:
        """
        return s is None or len(s) == 0 or s == "NA" or s == "N/A"

    def get_first_not_missing(self, fields, d):
        """
        Return value from first non-missing field. Useful for when a single field in the db
        can be alternatively populated with many possible alternatives drawn from other fields
        :param fields:
        :param d: dictionary to look for data
        :return: None if all are missing
        """
        for field in fields:
            if field in d and not self.is_missing(d[field]):
                return d[field]
        return None

    def consume_event(self, label):
        """ Account for events that signal the start of a new sequence of related events ('a play')"""
        if label in ['start game', 'win level', 'lose level', 'replay level']:
            self.play_id += 1


class JsonSpecimenParser(AbstractSpecimenParser):
    """
    Json to database parser for specimen data

    example usage:

    from specimen.database.dbtypes import *
    from specimen.database.parsers import *
    db = Database("my_db", [User, Device, Carrier, Session, Event, SelectionEvent, PurchaseEvent, LevelEvent], 1000, 20000)
    parser = JsonSpecimenParser(db)
    parser.parse("../Datasets/2016-06-03-to-2016-06-04")
    """
    def __init__(self, *args):
        super(JsonSpecimenParser, self).__init__(*args)

    # handle each of the events according to the label to create detailed records
    event_handlers = {
        "start game"        : lambda self, log, uId:  None,
        "select specimen"   : lambda self, log, uId: self.parse_selection_event(log, self.event_id, uId),
        "lose level"        : lambda self, log, uId: self.parse_level_event(log, self.event_id),
        "win level"         : lambda self, log, uId: self.parse_level_event(log, self.event_id),
        "replay level"      : lambda self, log, uId: self.parse_level_event(log, self.event_id),
        "purchase activity" : lambda self, log, uId: self.parse_purchase_event(log, self.event_id),
        "spectrum cleared"  : lambda self, log, uId:  None,
        "share press"       : lambda self, log, uId:  None,
    }

    def parse(self, file_name):
        """
        Take json file and parse contents into records. Inserts records into database.
        Note that entire file contents are brought into memory.
        :param file: json file
        :return:
        """
        # refresh necessary database info
        super(JsonSpecimenParser, self).get_state_info()

        # brings contents of entire file into memory for processing!
        print "Parsing %s" % file_name
        with open(file_name, 'r') as f:
            raw_data = f.read()
        raw_data = json.loads(raw_data)
        sessions = raw_data['sessionEvents']
        for session in sessions:
            user_rec = self.parse_user(session)
            device_rec = self.parse_device(session)
            carrier_rec = self.parse_carrier(session)
            session_rec = self.parse_session(session, self.session_id)
            self.db.insert(user_rec)
            self.db.insert(device_rec)
            self.db.insert(carrier_rec)
            self.db.insert(session_rec)
            logs = session['l']
            # all logs in current session belong to same user
            uniqueId = user_rec.uniqueId
            for log in logs:
                # make logs and params to use None value if missing to avoid failure
                safe_log = defaultdict(lambda: None, log)
                safe_log['p'] = defaultdict(lambda : None, safe_log['p'])
                event_rec = self.parse_event(safe_log, self.event_id, self.session_id)
                self.db.insert(event_rec)
                label = event_rec.event.lower().strip()
                handler = JsonSpecimenParser.event_handlers[label]
                details_rec = handler(self, safe_log, uniqueId)
                if details_rec:
                    self.db.insert(details_rec)
                self.event_id += 1
            # clear up for next user
            self.prev_target_color = None
            self.session_id += 1
        # make sure we flush any remaining records (as we may have inserted since last flush)
        self.db.flush()

    def parse_user(self, ss):
        uniqueId = ss['u']
        birthYear = ss['by']
        gender = ss['g']
        return User(uniqueId, birthYear, gender)

    def parse_device(self, ss):
        deviceName = ss['dm']
        return Device(deviceName)

    def parse_carrier(self, ss):
        carrierName = ss['cr']
        return Carrier(carrierName)

    def parse_session(self, ss, sessionId):
        uniqueId = ss['u']
        startTimestamp = ss['t']
        sessionLength = ss['len']
        version = ss['v']
        version = '-1' if len(version) == 0 else version
        country = ss['cy']
        carrierName = ss['cr']
        deviceName = ss['dm']
        lon = ss['lon']
        lat = ss['lat']
        return Session(sessionId, uniqueId, startTimestamp, sessionLength, version, country, carrierName, deviceName, lon, lat)

    def parse_event(self, log, eventId, sessionId):
        offsetTimestamp = log['o']
        label = log['e'].strip().lower()
        self.consume_event(label)
        return Event(eventId, sessionId, offsetTimestamp, label)

    def parse_selection_event(self, log, eventId, uniqueId):
        params = log['p']
        specimen_rgb = map(float, params['specimen_color'].strip("()").split(","))
        specimen_hsv = colorsys.rgb_to_hsv(*specimen_rgb)
        specimen_lab = utils.rgb_to_lab(*specimen_rgb)
        correct = False
        try:
            target_rgb = map(float, params['target_color'].strip("()").split(","))
            target_hsv = colorsys.rgb_to_hsv(*target_rgb)
            target_lab = utils.rgb_to_lab(*target_rgb)
        except (KeyError, AttributeError):
            # was correct selection
            target_rgb = specimen_rgb
            target_hsv = specimen_hsv
            target_lab = specimen_lab
            correct = True
        is_first_pick = self.prev_target_color != target_rgb
        # update the target color information
        self.prev_target_color = target_rgb
        pos_x = params['position_x']
        pos_y = params['position_y']
        return SelectionEvent(eventId, uniqueId, self.play_id, specimen_rgb, target_rgb, specimen_hsv, target_hsv, specimen_lab, target_lab, correct, pos_x, pos_y, is_first_pick)

    def parse_purchase_event(self, log, eventId):
        params = log['p']
        itemPurchased = params['Item Purchased']
        cost = self.get_first_not_missing(['Cost', 'Amount Spent'], params)
        return PurchaseEvent(eventId, cost, itemPurchased)

    def parse_level_event(self, log, eventId):
        params = log['p']
        spectrum = self.get_first_not_missing(['spectrum', 'Spectrum'], params).lower()
        level = params['level']
        score = self.get_first_not_missing(['score', 'Score'], params)
        boosterUsed = params['Booster Used'] == '1'
        return LevelEvent(eventId, spectrum, level, score, boosterUsed)


class CsvSpecimenParser(AbstractSpecimenParser):
    """
    Csv to database parser for specimen data. CSV files come from a slightly different source (Flurry) and
    have different information. We need to use stub values for some fields, and some values are parsed differently. This
    means it is important that you use the appropriate parser based on the source of the underlying data files
    (based on file type).

    example usage:

    from specimen.database.dbtypes import *
    from specimen.database.parsers import *

    db = Database("my_db", [User, Device, Carrier, Session, Event, SelectionEvent, PurchaseEvent, LevelEvent], 1000, 20000)
    parser = CsvSpecimenParser(db)
    parser.parse("../Datasets/Specimen-[2015_08_23-2015_08_24]-eventsLog.csv")
    """

    # relevant information for calculating timestamps from strings
    TIMESTAMP_FORMAT = "%b %d, %Y %I:%M %p"
    TIMESTAMP_START = datetime.utcfromtimestamp(0)

    def __init__(self, *args):
        super(CsvSpecimenParser, self).__init__(*args)
        self.line_num = 0
        # information used to track if we're in a new session in flat csv file
        self.prev_device = None
        self.prev_ts = None

    # handle each of the events according to the label
    event_handlers = {
        "start game"        : lambda self, line, uId:  None,
        "select specimen"   : lambda self, line, uId: self.parse_selection_event(line, self.event_id, uId),
        "lose level"        : lambda self, line, uId: self.parse_level_event(line, self.event_id),
        "win level"         : lambda self, line, uId: self.parse_level_event(line, self.event_id),
        "replay level"      : lambda self, line, uId: self.parse_level_event(line, self.event_id),
        "purchase activity" : lambda self, line, uId: self.parse_purchase_event(line, self.event_id),
        "spectrum cleared"  : lambda self, line, uId:  None,
        "share press"       : lambda self, line, uId:  None,
    }

    def parse(self, file_name):
        """
        Take csv file and parse contents into records. Inserts records into database.
        Files are brought into memory a line at a time.
        :param file: csv file
        :return:
        """
        # refresh necessary database info
        super(CsvSpecimenParser, self).get_state_info()
        self.prev_device = None
        self.prev_ts = None

        # all lines in a given csv file are assumed to be part of one giant session by the same
        # anonymous user
        print "Parsing file %s" % file_name
        with open(file_name, 'r') as f:
            # skip header row
            f.readline()
            self.line_num += 1
            for line in csv.reader(f):
                # there are some ill-formed records (such as "Maximum result limit reached")
                if len(line) < 9:
                    continue
                self.line_num +=1
                # parse params...annoying format
                line[8] = self.parse_params(line)
                user_rec = self.parse_user(line)
                device_rec = self.parse_device(line)
                carrier_rec = self.parse_carrier(line)

                # keep track if we're in a new session
                ts = self.__to_timestamp(line[0])
                # we habe to based this on a timestamp and a device, since user id
                # is not meaningful for CSVs
                if self.prev_device != device_rec.deviceName or ts != self.prev_ts:
                    self.prev_device = device_rec.deviceName
                    self.prev_ts = ts
                    self.session_id += 1
                    # reset session-specific information
                    self.prev_target_color = None
                    self.ts_offset = 0

                session_rec = self.parse_session(line, self.session_id)
                self.db.insert(user_rec)
                self.db.insert(device_rec)
                self.db.insert(carrier_rec)
                self.db.insert(session_rec)
                uniqueId = user_rec.uniqueId
                event_rec = self.parse_event(line, self.event_id, self.session_id)
                self.db.insert(event_rec)
                label = event_rec.event.lower().strip()
                handler = CsvSpecimenParser.event_handlers[label]
                details_rec = handler(self, line, uniqueId)
                if details_rec:
                    self.db.insert(details_rec)
                self.event_id += 1
                self.ts_offset += 1
        self.db.flush()

    def parse_user(self, line):
        # csv files do not have any user info, so we assign to a generic user id
        uniqueId = User.null
        birthYear = None
        gender = None
        return User(uniqueId, birthYear, gender)

    def parse_device(self, line):
        deviceName = line[6]
        return Device(deviceName)

    def parse_carrier(self, line):
        # csv files do not have any carrier info
        carrierName = None
        return Carrier(carrierName)

    def parse_session(self, line, sessionId):
        uniqueId = User.null
        startTimestamp = self.__to_timestamp(line[0])
        sessionLength = 0
        version = line[4]
        country = None
        carrierName = None
        deviceName = line[6]
        lon = None
        lat = None
        return Session(sessionId, uniqueId, startTimestamp, sessionLength, version, country, carrierName, deviceName, lon, lat)

    def parse_event(self, line, eventId, sessionId):
        # we keep a dummy timestamp offset, to provide order of events
        offsetTimestamp = self.ts_offset
        label = line[2].strip().lower()
        self.consume_event(label)
        return Event(eventId, sessionId, offsetTimestamp, label)

    def __to_timestamp(self, strdatetime):
        end = datetime.strptime(strdatetime, CsvSpecimenParser.TIMESTAMP_FORMAT)
         # convert to ms since unix epoch
        return (end - CsvSpecimenParser.TIMESTAMP_START).total_seconds() * 1000.0

    def parse_selection_event(self, line, eventId, uniqueId):
        params = line[8]
        specimen_rgb = map(float, params['specimen_color'].strip("()").split(","))
        specimen_hsv = colorsys.rgb_to_hsv(*specimen_rgb)
        specimen_lab = utils.rgb_to_lab(*specimen_rgb)
        correct = False
        try:
            target_rgb = map(float, params['target_color'].strip("()").split(","))
            target_hsv = colorsys.rgb_to_hsv(*target_rgb)
            target_lab = utils.rgb_to_lab(*target_rgb)
        except (KeyError, AttributeError):
            # was correct selection
            target_rgb = specimen_rgb
            target_hsv = specimen_hsv
            target_lab = specimen_lab
            correct = True
        is_first_pick = self.prev_target_color != target_rgb
        # update the target color information
        self.prev_target_color = target_rgb
        pos_x = params['position_x']
        pos_y = params['position_y']
        return SelectionEvent(eventId, uniqueId, self.play_id, specimen_rgb, target_rgb, specimen_hsv, target_hsv, specimen_lab, target_lab, correct, pos_x, pos_y, is_first_pick)

    def parse_purchase_event(self, line, eventId):
        params = line[8]
        itemPurchased = params['Item Purchased']
        cost = self.get_first_not_missing(['Cost', 'Amount Spent'], params)
        return PurchaseEvent(eventId, cost, itemPurchased)

    def parse_level_event(self, line, eventId):
        params = line[8]
        spectrum = self.get_first_not_missing(['spectrum', 'Spectrum'], params)
        spectrum = spectrum.lower() if spectrum else spectrum
        level = params['level']
        score = self.get_first_not_missing(['score', 'Score'], params)
        boosterUsed = params['Booster Used'] == '1'
        return LevelEvent(eventId, spectrum, level, score, boosterUsed)

    def parse_params(self, line):
        # annoying non-json format
        param_list = line[8].strip("{}").split(";")
        params = defaultdict(lambda : None, {})
        for param in param_list:
            (key, value) = param.split(":")
            params[key.strip()] = value.strip()
        return params