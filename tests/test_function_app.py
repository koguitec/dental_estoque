from unittest.mock import patch
import json
import azure.functions as func
from function_app import servicebus_queue_trigger_update_estoque

app = func.FunctionApp()


@patch("include.db.update_database")
@app.service_bus_queue_trigger(
    arg_name="azservicebus",
    queue_name="estoque",
    connection="dental_RootManageSharedAccessKey_SERVICEBUS",
    is_sessions_enabled=True,
)
def test_servicebus_queue_trigger_update_estoque(mock_update_database):
    # Simulate a message body
    message = {
        "codigoFilial": "001",
        "codigoERP": "A123",
        "saldo": 10,
        "custoProduto": 100,
    }
    azservicebus = func.ServiceBusMessage(body=json.dumps([message]))

    # Invoke the function
    servicebus_queue_trigger_update_estoque(azservicebus)

    # Assert that the database update was called with the correct payload
    mock_update_database.assert_called_once()
