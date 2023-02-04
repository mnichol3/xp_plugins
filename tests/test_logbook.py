"""
test_logbook.py

Unit tests for logbook plugin.
"""
import os
import sys
import unittest

import dummy_aircraft

try:
    import flight_phase
except:
    main_dir = os.path.join('..', 'logbook')
    sys.path.insert(1, main_dir)
    import flight_phase


class TestFlightPhase(unittest.TestCase):

    def setUp(self):
        self.aircraft = dummy_aircraft.DummyAircraft()
        self.flight_phase = flight_phase.FlightPhase(self.aircraft)

    def test_flight_point2point(self):
        """Nominal airliner flight profile"""
        self.assertEqual(self.flight_phase.phase, 'PHASE_RAMP')

        # Push back & start
        self.flight_phase._aircraft.set_eng_running(True)
        self.flight_phase._aircraft.set_speed_ground(0)
        self.flight_phase._aircraft.set_parking_brake(True)
        self.flight_phase.update()
        self.assertEqual(self.flight_phase.phase, 'PHASE_RAMP')

        # Taxi out
        self.flight_phase._aircraft.set_parking_brake(False)
        self.flight_phase._aircraft.set_speed_ground(5)
        self.flight_phase.update()
        self.assertEqual(self.flight_phase.phase, 'PHASE_TAXI_OUT')

        # Line up and wait
        self.flight_phase._aircraft.set_speed_ground(0)
        self.flight_phase.update()
        self.assertEqual(self.flight_phase.phase, 'PHASE_TAXI_OUT')

        # Takeoff roll
        self.flight_phase._aircraft.set_speed_ias(50)
        self.flight_phase.update()
        self.assertEqual(self.flight_phase.phase, 'PHASE_TAXI_OUT')

        # Takeoff
        self.flight_phase._aircraft.set_altitude_agl(200)
        self.flight_phase.update()
        self.assertEqual(self.flight_phase.phase, 'PHASE_TAKEOFF')

        # Climb out
        self.flight_phase._aircraft.set_speed_ias(100)
        self.flight_phase._aircraft.set_speed_vertical(500)
        self.flight_phase.update()
        self.assertEqual(self.flight_phase.phase, 'PHASE_CLIMB')

        # Cruise w/ some altitude adjustment
        self.flight_phase._aircraft.set_speed_ias(150)
        self.flight_phase._aircraft.set_speed_vertical(50)
        self.flight_phase.update()
        self.assertEqual(self.flight_phase.phase, 'PHASE_CRUISE')

        # Step climb
        self.flight_phase._aircraft.set_speed_vertical(500)
        self.flight_phase.update()
        self.assertEqual(self.flight_phase.phase, 'PHASE_CLIMB')

        # Descent
        self.flight_phase._aircraft.set_speed_vertical(-800)
        self.flight_phase.update()
        self.assertEqual(self.flight_phase.phase, 'PHASE_DESCENT')

        # Approach/final
        self.flight_phase._aircraft.set_speed_vertical(-700)
        self.flight_phase._aircraft.set_altitude_agl(200)
        self.flight_phase.update()
        self.assertEqual(self.flight_phase.phase, 'PHASE_LANDING')

        # Taxi in
        self.flight_phase._aircraft.set_wheels_on_ground(True)
        self.flight_phase._aircraft.set_speed_ground(5)
        self.flight_phase._aircraft.set_speed_ias(5)
        self.flight_phase.update()
        self.assertEqual(self.flight_phase.phase, 'PHASE_TAXI_IN')

        # Waiting to enter ramp
        self.flight_phase._aircraft.set_speed_ground(0)
        self.flight_phase._aircraft.set_speed_ias(0)
        self.flight_phase._aircraft.set_parking_brake(True)
        self.flight_phase.update()
        self.assertEqual(self.flight_phase.phase, 'PHASE_TAXI_IN')

        # Parked/shut down
        self.flight_phase._aircraft.set_eng_running(False)
        self.flight_phase.update()
        self.assertEqual(self.flight_phase.phase, 'PHASE_Ramp')


if __name__ == '__main__':
    unittest.main()
