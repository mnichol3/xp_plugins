"""
flight_phase.py

"""


class FlightPhase(object):
    """
    Class containing logic to determine the phase of flight an aircraft is in.

    Notes
    -----
    * Aircraft state units:
        * Altitude AGL: meters
        * Ground speed: meters/second
        * Speed IAS: knots
        * Vertical speed: feet/minute
    """
    PHASE_RAMP = 'PHASE_RAMP'
    PHASE_TAXI_OUT = 'PHASE_TAXI_OUT'
    PHASE_TAKEOFF = 'PHASE_TAKEOFF'
    PHASE_CLIMB = 'PHASE_CLIMB'
    PHASE_CRUISE = 'PHASE_CRUISE'
    PHASE_DESCENT = 'PHASE_DESCENT'
    PHASE_LANDING = 'PHASE_LANDING'
    PHASE_TAXI_IN = 'PHASE_TAXI_IN'

    def __init__(self, aircraft):
        """
        Parameters
        ----------
        aircraft : Aircraft class
        """
        self._aircraft = aircraft
        self._phase = self.PHASE_RAMP

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, new_phase):
        self._phase = new_phase

    def update(self):
        prev_phase = self._phase

        if self._phase == self.PHASE_RAMP:
            if self._aircraft.is_engine_running() and not self._aircraft.is_stopped():
                self._phase = self.PHASE_TAXI_OUT

        elif self._phase == self.PHASE_TAXI_OUT:
            if self._aircraft.speed_ias() > 35 and self._aircraft.altitude_agl() < 500:
                self._phase = self.PHASE_TAKEOFF

            elif (self._aircraft.is_on_ground() and
                    self._aircraft.is_stopped() and
                    not self._aircraft.is_engine_running()):
                self._phase = self.PHASE_RAMP

        elif self.phase == self.PHASE_TAKEOFF:
            if (self._aircraft.speed_vertical() > 200 and
                    self._aircraft.altitude_agl() >= 100):
                self._phase = self.PHASE_CLIMB

            elif (self._aircraft.verticalspeed() < -200 and
                    self._aircraft.altitude_agl() < 500):
                self._phase = self.PHASE_LANDING

        elif self.phase == self.PHASE_CLIMB:
            if abs(self._aircraft.speed_vertical()) < 200:
                self._phase = self.PHASE_CRUISE

            elif self._aircraft.speed_vertical() < -200:
                self._phase = self.PHASE_DESCENT

        elif self.phase == self.PHASE_CRUISE:
            if self._aircraft.speed_vertical() > 200:
                self._phase = self.PHASE_CLIMB

            elif self._aircraft.speed_vertical() < -500:
                self._phase = self.PHASE_DESCENT

        elif self.phase == self.PHASE_DESCENT:
            if self._aircraft.altitude_agl() <= 500:
                self._phase = self.PHASE_LANDING

        elif self.phase == self.PHASE_LANDING:
            # TODO: Add case for touch-n-go
            if self._aircraft.is_on_ground() and self._aircraft.speed_ground() < 35:
                self._phase = self.PHASE_TAXI_IN

            elif (self._aircraft.speed_vertical() > 200 and
                  self._aircraft.altitude_agl() >= 500):
                self._phase = self.PHASE_CLIMB

        elif self.phase == self.PHASE_TAXI_IN:
            if (self._aircraft.isonground() and
                    not self._aircraft.isenginerunning() and
                    self._aircraft.isstopped()):
                self._phase = self.PHASE_RAMP

            if (self._aircraft.speed_ias() > 35 and
                    self._aircraft.altitude_agl() < 500 and
                    self._aircraft.speed_vertical() > 200):
                self._phase = self.PHASE_TAKEOFF

        return self._phase == prev_phase
