import unittest
import csv
from main import app  # Note: You'll need to modify main.py to expose the app dictionary for testing

class TestDunderMifflinDemo(unittest.TestCase):
    def test_users(self):
        with open("csv/users.csv", newline='') as f:
            reader = csv.DictReader(f)
            users = {row["name"] for row in reader}
        app_users = {identity["name"] for identity in app["identities"] if identity["identity_type"] == "user"}
        self.assertEqual(users, app_users)

    def test_roles(self):
        with open("csv/roles.csv", newline='') as f:
            reader = csv.DictReader(f)
            roles = {row["name"] for row in reader}
        app_roles = {role["name"] for role in app["roles"]}
        self.assertEqual(roles, app_roles)

if __name__ == '__main__':
    unittest.main()
