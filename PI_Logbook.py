"""
PI_Logbook.py

A simple X-Plane logbook plugin.
"""
from datetime import datetime, timezone
from pathlib import Path

from XPPython3 import xp

from logbook.aircraft import Aircraft
from logbook.flight_log import FlightLog
from logbook.flight_phase import FlightPhase


class PythonInterface:

    def XPluginStart(self):
        self.Name = "Logbook v1.0"
        self.Sig = "xppython3.PI_Logbook"
        self.Desc = "A simple logbook."

        # The values of these variables can be changed to write the file
        # wherever you'd like.
        output_dir = Path(__file__).parent.joinpath('logbook')
        output_file = 'logbook.txt'

        # This variable determines whether to use sim time or system time.
        # Set to "sim" to sim time, or "system" to use system time.
        self.time_src = "sim"

        self.output_file = output_dir.joinpath(output_file)
        self.flight_log = FlightLog()
        self.flight_phase = FlightPhase(Aircraft)

        if self.time_src == 'sim':
            self.time_func = self.get_sim_time
        elif self.time_src == 'system':
            self.time_func = self.get_real_time
        else:
            raise ValueError(f'Invalid time_src value "{self.time_src}"')

        self.flight_log.aircraft_type = Aircraft.icao_type()
        self.flight_log.origin = Aircraft.nearest_airport()
        # TODO: try to get origin/dest from FMS

        # Register our FL callback with initial callback freq of 1 second
        xp.registerFlightLoopCallback(self.FlightLoopCallback, 1.0, 0)

        return self.Name, self.Sig, self.Desc

    def XPluginStop(self):
        # Unregister the callback
        xp.unregisterFlightLoopCallback(self.FlightLoopCallback, 0)

        # Close the file
        #self.output_file.close()
        self.flight_log.write(self.output_file)

    def XPluginEnable(self):
        return 1

    def XPluginDisable(self):
        # TODO: simple GUI to enable/disable
        pass

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        pass

    def FlightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):
        # TODO: Case for touch-n-go
        prev_phase = self.flight_phase.phase
        curr_phase = self.flight_phase.update()
        call_time = 3.0

        if prev_phase != curr_phase:
            # Increase callback frequency as things are happening
            call_time = 1.0
            time_local, time_zulu = self.time_func()

            if prev_phase == 'PHASE_RAMP' and curr_phase == 'PHASE_TAXI_OUT':
                self.flight_log.mark_time('out', time_local, time_zulu)

            elif prev_phase == 'PHASE_TAXI_OUT' and curr_phase == 'PHASE_TAKEOFF':
                self.flight_log.mark_time('off', time_local, time_zulu)

            elif prev_phase == 'PHASE_LANDING':
                if curr_phase == 'PHASE_TAXI_IN':
                    self.flight_log.mark_time('on', time_local, time_zulu)
                    self.flight_log.calc_air_time()
                elif curr_phase == 'PHASE_CLIMB':
                    # touch-and-go
                    # How do we differentiate go-around from actual touch & go?
                    pass
                self.flight_log.inc_landing_count()

            elif prev_phase == 'PHASE_TAXI_IN' and curr_phase == 'PHASE_RAMP':
                self.flight_log.mark_time('in', time_local, time_zulu)
                self.flight_log.calc_block_time()
                self.flight_log.destination = Aircraft.nearest_airport()

        # Return value sets next call time, in seconds
        return call_time

    def get_real_time(self):
        """
        Get the current real-world time, as the total number of seconds
        since midnight.

        Returns
        -------
        int, int
            Local and zulu time
        """
        time_local = datetime.now().time()
        time_local = self.total_time(time_local)

        time_zulu = datetime.now(tz=timezone.utc).time()
        time_zulu = self.total_time(time_zulu)

        return time_local, time_zulu

    def get_sim_time(self):
        """
        Get the current time of day in the simulator, as the total number
        of seconds since midnight.

        Returns
        -------
        int, int
            Local and zulu time
        """
        time_local = xp.getDatai("sim/time/local_time_sec")
        time_zulu = xp.getDatai("sim/time/zulu_time_sec")

        return time_local, time_zulu

    @staticmethod
    def total_time(dt):
        """
        Return the time from a Datetime object as the total number of seconds
        since midnight.

        Parameters
        ----------
        dt : Datetime object

        Returns
        -------
        int
        """
        total = dt.hour * 3600
        total += dt.minute * 60
        total += dt.second

        return total
