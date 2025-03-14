import unittest
from itertools import count

from src.ship import Ship
class TestShipInitialization(unittest.TestCase):

    def setUp(self):
        pass

    def test_creation(self):
        ship1 = Ship("Rotterdam", 7)
        self.assertIsInstance(ship1, Ship)

    def test_initialization(self):
        ship1 = Ship("Rotterdam", 7)
        self.assertEqual(ship1.destination, "Rotterdam")
        self.assertEqual(ship1.voyage_duration, 7)

    def test_calculate_fuel(self):
        ship1 = Ship("Rotterdam",7)
        ship2 = Ship("Singapore",5)
        ship3 = Ship("Singapore",0)
        self.assertEqual(ship1.calculate_fuel(),700)
        self.assertEqual(ship2.calculate_fuel(),500)
        self.assertEqual(ship3.calculate_fuel(),0)

    def test_add_crew_member(self):
        ship1 = Ship("Rotterdam",7)
        ship1.add_crew_member("Captain Smith")
        ship1.add_crew_member("Captain Smith")

        ship1.add_crew_member("First Mate Jones")
        ship1.add_crew_member("Engineer Roberts")

        self.assertIn("Captain Smith",ship1.crew_member)
        self.assertIn("First Mate Jones",ship1.crew_member)
        self.assertIn("Engineer Roberts",ship1.crew_member)

        self.assertEqual(ship1.crew_member.count("Captain Smith"), 2)

    def test_add_empty_crew_member(self):
        ship1 = Ship("Rotterdam", 7)
        with self.assertRaises(ValueError):
            ship1.add_crew_member("")

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()