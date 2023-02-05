"""
flight_log.py

Class to represent a single entry in the flight logbook.
"""
from datetime import datetime, timedelta


class FlightLog:
    """
    Class to represent a single entry in the logbook.

    Notes
    ------
    * Using None for unset time variables instead of 0 since its
      possible for 0 to be a valid event time.
      Ex: taking off exactly at midnight.
    """

    def __init__(self):
        self._date = datetime.now().strftime('%Y-%m-%d')
        self._acft_type = None
        self._acft_reg = None
        self._call_sign = None

        self._origin = None
        self._dest = None

        self._out_local = None
        self._off_local = None
        self._on_local = None
        self._in_local = None

        self._out_zulu = None
        self._off_zulu = None
        self._on_zulu = None
        self._in_zulu = None

        self._air_time = None
        self._block_time = None

        self._num_landings = 0
        self._num_landings_night = 0

    @property
    def aircraft_type(self):
        return self._acft_type

    @aircraft_type.setter
    def aircraft_type(self, acft_type):
        self._acft_type = acft_type

    @property
    def aircraft_reg(self):
        return self._acft_reg

    @aircraft_reg.setter
    def aircraft_reg(self, reg):
        self._acft_reg = reg

    @property
    def air_time(self):
        return self._air_time

    @air_time.setter
    def air_time(self, air_time):
        self._air_time = air_time

    @property
    def block_time(self):
        return self._block_time

    @block_time.setter
    def block_time(self, block_time):
        self._block_time = block_time

    @property
    def date(self):
        return self._date

    @property
    def destination(self):
        return self._dest

    @destination.setter
    def destination(self, dest):
        self._dest = dest

    @property
    def landings(self):
        return self._num_landings

    @property
    def night_landings(self):
        return self._num_landings_night

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, origin):
        self._origin = origin

    def calc_air_time(self):
        #return self._calc_time_diff('air')
        self._air_time = self._calc_time_diff('air')

    def calc_block_time(self):
        #return self._calc_time_diff('block')
        self._block_time = self._calc_time_diff('block')

    def _calc_time_diff(self, time_kword):
        """
        Calculate the difference in time between two time variables.

        Parameters
        ----------
        time_kword : str
            Time to calculate, i.e. 'air' for air time or 'blocl' for block time.

        Returns
        -------
        float
        """
        if time_kword == 'air':
            time1 = self._off_zulu
            time2 = self._on_zulu
        elif time_kword == 'block':
            time1 = self._out_zulu
            time2 = self._in_zulu
        else:
            raise ValueError(f'Invalid time_kword argument {time_kword}')

        try:
            time_diff = time2 - time1
        except TypeError:
            # One or more of the time variables needed have not been set
            return

        if time_diff < 0:
            time_diff += (24 * 3600)

        return FlightLog.seconds2hours(time_diff)

    def get_timestrings_local(self):
        t_out = FlightLog.seconds2hours_str(self._out_local)
        t_off = FlightLog.seconds2hours_str(self._off_local)
        t_on = FlightLog.seconds2hours_str(self._on_local)
        t_in = FlightLog.seconds2hours_str(self._in_local)

        return t_out, t_off, t_on, t_in

    def inc_landing_count(self, night=False):
        if night:
            self._num_landings_night += 1
        else:
            self._num_landings += 1

    def mark_time(self, time_var, time_local, time_zulu):
        """
        Set the local & zulu times of a given aircraft event.

        Parameters
        ----------
        time_var : str
            Time variable to set.
        time_local : int
            Seconds since midnight in sim local time.
        time_zulu : int
            Seconds since midnight in sim zulu time.

        Returns
        -------
        None.
        """
        time_local = self.seconds2hours_str(time_local)
        time_zulu = self.seconds2hours_str(time_zulu)

        match time_var:
            case 'out':
                self._out_local = time_local
                self._out_zulu = time_zulu
            case 'off':
                self._off_local = time_local
                self._off_zulu = time_zulu
            case 'on':
                self._on_local = time_local
                self._on_zulu = time_zulu
            case 'in':
                self._in_local = time_local
                self._in_zulu = time_zulu
            case _:
                raise ValueError(f'Invalid timeVar argument {time_var}')

    @staticmethod
    def seconds2hours(seconds):
        """
        Convert an amount of seconds to hours. Returned as a float rounded to
        2 decimal places.

        Parameters
        ----------
        seconds : int

        Returns
        -------
        float
        """
        return round(seconds / 3600, 2)

    @staticmethod
    def seconds2hours_str(seconds):
        """
        Convert an amount of seconds to hours and minutes.
        Format: HH:MM.

        Parameters
        ----------
        seconds : int

        Returns
        -------
        str
        """
        try:
            time_str = str(timedelta(seconds=seconds)).zfill(8)[:5]
        except TypeError:
            time_str = None

        return time_str

    def write(self, output_file):
        """
        Write the log as a CSV.

        Parameters
        ----------
        output_file : pathlib.Path

        Returns
        -------

        """
        log_attrs = {
            'date': '_date',
            'acft_type': '_acft_type',
            'origin': '_origin',
            'destination': '_dest',
            'out_local': '_out_local',
            'off_local': '_off_local',
            'on_local': '_on_local',
            'in_local': '_in_local',
            'out_zulu': '_out_zulu',
            'off_zulu': '_off_zulu',
            'on_zulu': '_on_zulu',
            'in_zulu': '_in_zulu',
            'air_time': '_air_time',
            'block_time': '_block_time',
            'num_landings': '_num_landings',
        }

        log_vals = [getattr(self, x) for x in log_attrs.values()]
        log_vals = [x if x is not None else 'NA' for x in log_vals]
        log_line = ','.join(log_vals)

        if output_file.is_file():
            with open(output_file, 'a') as f_out:
                f_out.write(log_line + '\n')
        else:
            hdr_line = ','.join(list(log_attrs.keys()))
            with open(output_file, 'w') as f_out:
                f_out.write(hdr_line + '\n')
                f_out.write(log_line + '\n')
