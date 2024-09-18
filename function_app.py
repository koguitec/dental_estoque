import azure.functions as func
import json
import logging

from .include.db import update_database
from .helpers import order_items

logger = logging.getLogger(__name__)

app = func.FunctionApp()


@app.service_bus_queue_trigger(
    arg_name="azservicebus",
    queue_name="estoque",
    connection="dental_RootManageSharedAccessKey_SERVICEBUS",
    is_sessions_enabled=True,
)
def servicebus_queue_trigger_update_estoque(azservicebus: func.ServiceBusMessage):
    logger.info(
        "Python ServiceBus Queue trigger processed a message: %s",
        azservicebus.get_body().decode("utf-8"),
    )

    # # Parse the message body
    # message = azservicebus.get_body().decode("utf-8")

    # # Assuming the message body contains a list of items in JSON format
    # try:
    #     payload = json.loads(message)
    # except json.JSONDecodeError as e:
    #     logger.error(f"Failed to decode the message body: {e}")
    #     return

    # # Order the payment data
    # ordered_data = order_items(payload)

    # # Update the database
    # try:
    #     update_database(ordered_data)
    # except Exception as e:
    #     logger.error(f"Failed to update database: {e}")
