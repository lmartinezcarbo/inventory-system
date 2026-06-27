import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from database import create_table, get_connection
from inventory_service import add_product, delete_product, get_products, update_stock


class InventoryCrudTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_inventory.db"
        create_table(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_crud_flow(self):
        add_product("Laptop", 3, 999.99, "Electronics", self.db_path)
        products = get_products(self.db_path)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0][1], "Laptop")

        update_stock(products[0][0], 5, self.db_path)
        updated = get_products(self.db_path)
        self.assertEqual(updated[0][2], 5)

        delete_product(products[0][0], self.db_path)
        self.assertEqual(get_products(self.db_path), [])


if __name__ == "__main__":
    unittest.main()
