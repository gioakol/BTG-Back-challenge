import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from botocore.exceptions import ClientError
from main import app

class TestClientRoutes(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("app.database.clients.table.get_item")
    def test_get_client_by_id_success(self, mock_get_item):
        mock_get_item.return_value = {
            "Item": {
                "amount": 500000,
                "idClient": "1",
                "fullName": "Giovanni Beltran Avila",
                "email": "gioakol@gmail.com",
                "phone": "+573229702531"
            }
        }

        response = self.client.get("clients/get/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "amount": 500000,
            "idClient": "1",
            "fullName": "Giovanni Beltran Avila",
            "email": "gioakol@gmail.com",
            "phone": "+573229702531"
        })

    @patch("app.database.clients.table.get_item")
    def test_get_client_by_id_not_found(self, mock_get_item):
        # Mocking DynamoDB response with no item
        mock_get_item.return_value = {}

        response = self.client.get("clients/get/1")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "El cliente al que intenta acceder no se encuentra."})


    @patch("app.database.clients.table.get_item")
    def test_get_client_by_id_server_error(self, mock_get_item):
        # Configura el mock para lanzar una excepción de error interno
        mock_get_item.side_effect = ClientError(
            {"Error": {"Message": "Internal Server Error"}}, 
            "GetItem"
        )

        response = self.client.get("clients/get/1")
        
        # Verifica el código de estado y el mensaje de error
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": "Internal Server Error"})


if __name__ == '__main__':
    unittest.main()
