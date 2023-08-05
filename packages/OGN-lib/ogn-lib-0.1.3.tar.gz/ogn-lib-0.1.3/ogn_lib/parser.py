import collections
import functools
import logging
from datetime import datetime, time, timedelta

from ogn_lib import constants, exceptions


FEET_TO_METERS = 0.3048
KNOTS_TO_MS = 1852 / 3600  # ratio between nautical knots and m/s
HPM_TO_DEGS = 180 / 60  # ratio between half turn per minute and degrees per s

TD_1DAY = timedelta(days=1)


logger = logging.getLogger(__name__)


class ParserBase(type):
    """
    Metaclass for all parsers.
    """

    parsers = {}
    default = None

    def __new__(meta, name, bases, dct):
        """
        Creates a new ParserBase class.

        Class callsigns are registered using the `__destto__` field of every
        class. If `__destto__` is not set, class name is used instead.
        """

        class_ = super().__new__(meta, name, bases, dct)
        callsigns = dct.get('__destto__', name)
        default = dct.get('__default__', False)

        if isinstance(callsigns, str):
            logger.debug('Setting %s as a parser for %s messages', name, callsigns)
            meta.parsers[callsigns] = class_
        elif isinstance(callsigns, collections.Sequence):
            for c in callsigns:
                logger.debug('Setting %s as a parser for %s messages', name, c)
                meta.parsers[c] = class_
        else:
            raise TypeError('instance of __destto__ should be either a sequence'
                            'or a string; is {}'.format(type(callsigns)))

        if default:
            meta.default = class_

        return class_

    @classmethod
    def __call__(cls, raw_message):
        """
        Parses the fields of a raw APRS message to a dictionary by calling the
        underlying method ParserBase._parse_message.

        :param str raw_message: raw APRS message
        :return: parsed message
        :rtype: dict
        :raises ogn_lib.exceptions.ParserNotFoundError: if parser for this
            message's callsign was not found
        """

        try:
            _, body = raw_message.split('>', 1)
            destto, *_ = body.split(',', 1)

            if 'TCPIP*' in body or ':>' in body or 'qAC' in body:  # server message
                return ServerParser.parse_message(raw_message)

            try:
                parser = cls.parsers[destto]
                logger.debug('Using %s parser for %s', parser, raw_message)
            except KeyError:
                logger.warn('Parser for a destto name %s not found; found: %s',
                            destto, list(cls.parsers.keys()))

                if cls.default:
                    parser = cls.default
                else:
                    raise exceptions.ParserNotFoundError(
                        'Parser for a destto name {} not found; found: {}'
                        .format(destto, list(cls.parsers.keys())))

            return parser.parse_message(raw_message)

        except exceptions.ParserNotFoundError:
            raise
        except Exception as e:
            msg = 'Failed to parse message: {}'.format(raw_message)
            logger.error(msg)
            logger.exception(e)
            raise exceptions.ParseError(msg)


class Parser(metaclass=ParserBase):
    """
    Base class for all parser classes.

    Implements parsing of APRS message header and calls the populates the data
    with the values returned by the _parse_comment(comment) of the extending
    class.
    """

    __default__ = True

    @classmethod
    def parse_message(cls, raw_message):
        """
        Parses the fields of a raw APRS message to a dictionary.

        :param str raw_message: raw APRS message
        :return: parsed message
        :rtype: dict
        """

        from_, body = raw_message.split('>', 1)
        header, *comment = body.split(' ', 1)

        data = {
            'from': from_,
            'beacon_type': constants.BeaconType.aircraft_beacon
        }
        data.update(Parser._parse_header(header))

        if comment:
            comment_data = cls._parse_comment(comment[0])

            try:
                cls._update_data(data, comment_data['_update'])
                del comment_data['_update']
            except KeyError:
                logger.debug('comment_data[\'_update\'] not set')

            data.update(comment_data)

        data['raw'] = raw_message
        return data

    @staticmethod
    def _parse_header(header):
        """
        Parses the APRS message header.

        :param str header: APRS message between the '[callsign]>' and comment
                           field
        :param str pos_separator: separator for latitude and longitude
        :param str attrs_separator: separator for attributes substring
        :return: parsed header
        :rtype: dict
        """

        col_idx = header.find(':')
        origin = header[:col_idx]
        position = header[col_idx + 2:]

        data = Parser._parse_origin(origin)
        data.update(Parser._parse_position(position))

        return data

    @staticmethod
    def _parse_origin(header):
        """
        Parses the destto, receiver and relayer field of the APRS message.
        :param str header: APRS message between the '[callsign]>' and position
                           information
        :return: parsed origin part of the APRS message
        :rtype: dict
        """

        fields = header.split(',')

        if len(fields) == 3:  # standard message
            relayer = None
        elif len(fields) == 4:  # relayed message
            relayer = fields[1].strip('*')
        else:
            raise ValueError('Unknown header format: {}'.format(header))

        data = {'destto': fields[0], 'receiver': fields[-1], 'relayer': relayer}

        return data

    @staticmethod
    def _parse_position(pos_header):
        """
        Parses the position information, timestamp, altitude, heading and
        ground speed from an APRS message.

        :param str pos_header: position part of the APRS header
        :param str pos_separator: separator for latitude and longitude
        :param str attrs_separator: separator for attributes substring
        :return: parsed position part of the APRS message
        :rtype: dict
        """

        timestamp = pos_header[0:7]
        lat = pos_header[7:15]
        lon = pos_header[16:25]
        attrs = pos_header[26:]

        data = {
            'timestamp': Parser._parse_timestamp(timestamp),
            'latitude': Parser._parse_location(lat),
            'longitude': Parser._parse_location(lon),
        }
        data.update(Parser._parse_attributes(attrs))

        return data

    @staticmethod
    def _parse_attributes(attributes):
        """
        Parses the APRS attributes for heading, ground speed and altitude.

        :param str attributes: attributes part of the APRS message
        :return: parsed attributes
        :rtype: dict
        """

        attrs = attributes.split('/')
        data = {}

        if attrs[-1].startswith('A='):  # has altitude
            data['altitude'] = int(attrs[-1][2:]) * FEET_TO_METERS
        else:
            data['altitude'] = None

        if len(attrs) > 1 and attributes[0] != '/':  # i.e., format is hdg/gsp/?
            heading = int(attrs[0])
            speed = int(attrs[1])
        else:
            heading = None
            speed = None

        if heading or speed:
            data['heading'] = heading
            data['ground_speed'] = speed * KNOTS_TO_MS
        else:
            data['heading'] = None
            data['ground_speed'] = None

        return data

    @staticmethod
    def _parse_timestamp(timestamp_str):
        """
        Parses the UTC timestamp of an APRS package.

        :param timestamp_str: utc timestamp string in %H%M%S or %d%H%M format
        :return: parsed timestamp
        :rtype: datetime.datetime
        """

        ts_str = timestamp_str[:6]
        type_ = timestamp_str[-1]

        if type_ == 'h':
            return Parser._parse_time(ts_str)
        else:
            return Parser._parse_datetime(ts_str)

    @staticmethod
    def _parse_time(timestamp):
        """
        Parses the HMS formated timestamp string.

        :param timestamp_str: utc timestamp string in %H%M%S
        :return: parsed timestamp
        :rtype: datetime.datetime
        """

        ts = time(*map(lambda x: int(x),
                       map(lambda x: timestamp[x * 2: x * 2 + 2], range(3))))
        full_ts = datetime.combine(datetime.utcnow(), ts)

        now = datetime.utcnow()

        td = (now - full_ts).total_seconds()
        if td < -300:
            full_ts -= TD_1DAY

        return full_ts

    @staticmethod
    def _parse_datetime(timestamp):
        """
        Parses the HMS formated timestamp string.

        :param timestamp_str: utc timestamp string in %H%M%S
        :return: parsed timestamp
        :rtype: datetime.datetime
        """

        ts = list(map(lambda x: int(x),
                      map(lambda x: timestamp[x * 2: x * 2 + 2], range(3))))

        now = datetime.now()
        date_ = datetime(now.year, now.month, ts[0])
        time_ = time(ts[1], ts[2], 0)

        full_ts = datetime.combine(date_, time_)

        return full_ts

    @staticmethod
    def _parse_location(location_str):
        """
        Parses the location string and returns a signed decimal position.

        :param location_str: location string in the standard APRS format
        :return: signed decimal latitude/longitude
        :rtype: float
        """

        sphere = location_str[-1]
        offset = 2 if sphere in ('N', 'S') else 3

        location = int(location_str[:offset])
        location += float(location_str[offset:offset + 5]) / 60

        if sphere in ('S', 'W'):
            location *= -1

        return location

    @staticmethod
    def _parse_comment(comment):
        """
        Parses the comment string from APRS messages.

        :param str comment: comment string
        :return: parsed comment
        :rtype: dict
        """

        logger.warn('Parser._parse_comment method not overriden')
        return {}

    @staticmethod
    def _get_location_update_func(update_with):
        """
        Builds a partial function for updating location with 3rd additional
        decimal.

        :param int update_with: 3rd decimal
        :return: partial function updating position with 3rd digit
        :rtype: callable
        """

        return functools.partial(Parser._update_location_decimal,
                                 update=update_with)

    @staticmethod
    def _update_location_decimal(existing, update):
        """
        Updates location with 3rd additional decimal.

        :param float existing: existing value
        :param int update: 3rd decimal
        :return: new location
        :rtype: float
        """

        delta = update
        if existing < 0:
            delta *= -1

        return existing + delta / 60000

    def _update_data(data, updates):
        """
        Updates the existing data with values described in `updates`.

        Updates are a list of dictionaries. Each dictionary should have two
        keys: `target` that contains the key from `data` which should be
        updated, and `function` which describes the update function.

        :param dict data: existing data
        :param list updates: list of updates
        :return: updated data
        :rtype: dict
        """

        for update in updates:
            try:
                key = update['target']
                value = data[key]
                data[key] = update['function'](value)
            except KeyError:
                logger.error('Key for update %s not found', update['target'])

        return data


class APRS(Parser):
    """
    Parser for the orignal OGN-flavoured APRS messages.
    """

    __destto__ = ['APRS', 'OGFLR', 'OGNTRK']

    FLAGS_STEALTH = 1 << 7
    FLAGS_DO_NOT_TRACK = 1 << 6
    FLAGS_AIRCRAFT_TYPE = 0b1111 << 2
    FLAGS_ADDRESS_TYPE = 0b11

    @staticmethod
    def _parse_comment(comment):
        """
        Parses the comment string from APRS messages.

        :param str comment: comment string
        :return: parsed comment
        :rtype: dict
        """

        data = {}
        fields = comment.split(' ')
        for field in fields:
            if field.startswith('!') and field.endswith('!'):  # 3rd decimal
                lat_dig = int(field[2])
                lon_dig = int(field[3])
                update_position = [
                    {
                        'target': 'latitude',
                        'function': Parser._get_location_update_func(lat_dig)
                    }, {
                        'target': 'longitude',
                        'function': Parser._get_location_update_func(lon_dig)
                    }
                ]
                try:
                    for u in update_position:
                        data['_update'].append(u)
                except KeyError:
                    data['_update'] = update_position
            elif field.startswith('id'):
                data.update(APRS._parse_id_string(field[2:]))
            elif field.endswith('fpm'):  # vertical speed
                data['vertical_speed'] = int(field[:-3]) * FEET_TO_METERS
            elif field.endswith('rot'):  # turn rate
                data['turn_rate'] = float(field[:-3]) * HPM_TO_DEGS
            elif field.startswith('FL'):  # (optional) flight level
                data['flight_level'] = float(field[2:])
            elif field.endswith('dB'):  # signal to noise ratio
                data['signal_to_noise_ratio'] = float(field[:-2])
            elif field.endswith('e'):  # error count
                data['error_count'] = int(field[:-1])
            elif field.endswith('kHz'):  # frequency offset
                data['frequency_offset'] = float(field[:-3])
            elif field.startswith('gps'):  # (optional) gps quality
                x_idx = field.find('x')
                data['gps_quality'] = {
                    'vertical': int(field[x_idx + 1:]),
                    'horizontal': int(field[3:x_idx])
                }
            elif field.startswith('s'):  # (optional) flarm software version
                data['flarm_software'] = field[1:]
            elif field.startswith('r'):  # (optional) flarm id
                data['flarm_id'] = field[1:]
            elif field.endswith('dBm'):  # (optional) power ratio
                data['power_ratio'] = float(field[:-3])
            elif field.startswith('hear'):  # (optional) other devices heard
                try:
                    data['other_devices'].append(field[4:])
                except KeyError:
                    data['other_devices'] = [field[4:]]
            elif field.startswith('h'):  # (optional) flarm hardware version
                data['flarm_hardware'] = int(field[1:], 16)

        return data

    @staticmethod
    def _parse_id_string(id_string):
        """
        Parses the information encoded in the id string.

        :param str id_string: unique identification string
        :return: parsed information
        :rtype: dict
        """

        flags = int(id_string[:2], 16)
        return {
            'uid': id_string,
            'stealth': bool(flags & APRS.FLAGS_STEALTH),
            'do_not_track': bool(flags & APRS.FLAGS_DO_NOT_TRACK),
            'aircraft_type': constants.AirplaneType(
                (flags & APRS.FLAGS_AIRCRAFT_TYPE) >> 2),
            'address_type': constants.AddressType(flags & APRS.FLAGS_ADDRESS_TYPE)
        }


class Naviter(Parser):
    """
    Parser for the Naviter-formatted APRS messages.
    """

    __destto__ = ['OGNAVI', 'OGNAVI-1']

    FLAGS_STEALTH = 1 << 15
    FLAGS_DO_NOT_TRACK = 1 << 14
    FLAGS_AIRCRAFT_TYPE = 0b1111 << 10
    FLAGS_ADDRESS_TYPE = 0b111111 << 4

    @staticmethod
    def _parse_comment(comment):
        """
        Parses the comment string from Naviter's APRS messages.

        :param str comment: comment string
        :return: parsed comment
        :rtype: dict
        """

        data = {}
        fields = comment.split(' ')
        for field in fields:
            if field.startswith('!') and field.endswith('!'):  # 3rd decimal
                lat_dig = int(field[2])
                lon_dig = int(field[3])
                update_position = [
                    {
                        'target': 'latitude',
                        'function': Parser._get_location_update_func(lat_dig)
                    }, {
                        'target': 'longitude',
                        'function': Parser._get_location_update_func(lon_dig)
                    }
                ]
                try:
                    for u in update_position:
                        data['_update'].append(u)
                except KeyError:
                    data['_update'] = update_position
            elif field.startswith('id'):
                data.update(Naviter._parse_id_string(field[2:]))
            elif field.endswith('fpm'):  # vertical speed
                data['vertical_speed'] = int(field[:-3]) * FEET_TO_METERS
            elif field.endswith('rot'):  # turn rate
                data['turn_rate'] = float(field[:-3]) * HPM_TO_DEGS

        return data

    @staticmethod
    def _parse_id_string(id_string):
        """
        Parses the information encoded in the id string.

        :param str id_string: unique identification string
        :return: parsed information
        :rtype: dict
        """

        flags = int(id_string[:4], 16)
        return {
            'uid': id_string,
            'stealth': bool(flags & Naviter.FLAGS_STEALTH),
            'do_not_track': bool(flags & Naviter.FLAGS_DO_NOT_TRACK),
            'aircraft_type': constants.AirplaneType(
                (flags & Naviter.FLAGS_AIRCRAFT_TYPE) >> 10),
            'address_type': constants.AddressType(
                (flags & Naviter.FLAGS_ADDRESS_TYPE) >> 4)
        }


class ServerParser:
    """
    Parser for server messages.
    """

    @staticmethod
    def parse_message(raw_message):
        """
        Passes a server message to an appropriate parser.

        :param raw_message: APRS message
        :return: parsed data
        :rtype: dict
        """

        if 'CPU' in raw_message or ':>' in raw_message:
            data = ServerParser.parse_status(raw_message)
        else:
            data = ServerParser.parse_beacon(raw_message)

        data['raw'] = raw_message
        return data

    @staticmethod
    def parse_beacon(raw_message):
        """
        Parses server beacon messages.

        :param raw_message: APRS message
        :return: parsed data
        :rtype: dict
        """

        from_, header = raw_message.split('>', 1)
        position, *comment = header.split(' ', 1)

        data = {
            'from': from_,
            'beacon_type': constants.BeaconType.server_beacon
        }

        data.update(Parser._parse_header(position))

        data['comment'] = comment[0] if comment else None

        return data

    @staticmethod
    def parse_status(raw_message):
        """
        Parses server status messages.

        :param raw_message: APRS message
        :return: parsed data
        :rtype: dict
        """

        from_, body = raw_message.split('>', 1)
        header, comment = body.split(' ', 1)

        sep_idx = header.find(':')
        origin = header[:sep_idx]
        timestamp = header[sep_idx + 2:sep_idx + 9]

        data = {
            'from': from_,
            'beacon_type': constants.BeaconType.server_status
        }

        data.update(Parser._parse_origin(origin))
        data['timestamp'] = Parser._parse_timestamp(timestamp)
        data['comment'] = comment

        return data
