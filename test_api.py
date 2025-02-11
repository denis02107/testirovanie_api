import unittest
import requests

BASE_URL = 'http://localhost:5000'


class TestItemsAPI(unittest.TestCase):

    def setUp(self):
        requests.post(f"{BASE_URL}/reset")

    def test_get_items_empty(self):
        response = requests.get(f"{BASE_URL}/items")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_create_item(self):
        data = {'name': 'Test Item'}
        response = requests.post(f"{BASE_URL}/items", json=data)
        self.assertEqual(response.status_code, 201)
        item = response.json()
        self.assertIn('id', item)
        self.assertEqual(item['name'], 'Test Item')

        # Проверка получения элемента по id
        item_id = item['id']
        response_get = requests.get(f"{BASE_URL}/items/{item_id}")
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_get.json(), item)

    def test_update_item(self):
        data = {'name': 'Old Name'}
        response = requests.post(f"{BASE_URL}/items", json=data)
        self.assertEqual(response.status_code, 201)
        item = response.json()
        item_id = item['id']

        new_data = {'name': 'New Name'}
        response_put = requests.put(f"{BASE_URL}/items/{item_id}", json=new_data)
        self.assertEqual(response_put.status_code, 200)
        updated_item = response_put.json()
        self.assertEqual(updated_item['id'], item_id)
        self.assertEqual(updated_item['name'], 'New Name')

    def test_delete_item(self):
        # Создаем элемент
        data = {'name': 'Item to Delete'}
        response = requests.post(f"{BASE_URL}/items", json=data)
        self.assertEqual(response.status_code, 201)
        item = response.json()
        item_id = item['id']

        # Удаляем элемент
        response_del = requests.delete(f"{BASE_URL}/items/{item_id}")
        self.assertEqual(response_del.status_code, 204)

        # Проверяем, что элемент не найден
        response_get = requests.get(f"{BASE_URL}/items/{item_id}")
        self.assertEqual(response_get.status_code, 404)

    def test_create_item_missing_name(self):
        data = {}
        response = requests.post(f"{BASE_URL}/items", json=data)
        self.assertEqual(response.status_code, 400)

    def test_update_item_not_found(self):
        new_data = {'name': 'Non-existent'}
        response = requests.put(f"{BASE_URL}/items/9999", json=new_data)
        self.assertEqual(response.status_code, 404)

    def test_delete_item_not_found(self):
        response = requests.delete(f"{BASE_URL}/items/9999")
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
