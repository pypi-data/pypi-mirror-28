import unittest

from mercedesapi import MercedesApi



class MyTestCase(unittest.TestCase):
    def test_something(self):
        mercedesApi = MercedesApi("PUT_YOUR_ACCESS_KEY_HERE")
        vehicles_id = mercedesApi.get_vehicle_ids()
        print(vehicles_id)

        vehicle_id = vehicles_id[0]['id']
        print(mercedesApi.get_vehicle_information(vehicle_id))
        print(mercedesApi.get_tire_state(vehicle_id))
        print(mercedesApi.get_location(vehicle_id))
        print(mercedesApi.get_odometer(vehicle_id))
        print(mercedesApi.get_fuel_state(vehicle_id))
        print(mercedesApi.get_charge_state(vehicle_id))
        print(mercedesApi.get_doors_state(vehicle_id))
        print(mercedesApi.lock_doors(vehicle_id))
        print(mercedesApi.get_doors_state(vehicle_id))
        print(mercedesApi.unlock_doors(vehicle_id))
        print(mercedesApi.get_doors_state(vehicle_id))


if __name__ == '__main__':
    unittest.main()
