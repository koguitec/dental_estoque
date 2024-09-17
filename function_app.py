import azure.functions as func
import logging

app = func.FunctionApp()


@app.service_bus_queue_trigger(
    arg_name="azservicebus",
    queue_name="estoque",
    connection="dental_RootManageSharedAccessKey_SERVICEBUS",
    is_session_enabled=True,
)
def servicebus_queue_trigger_update_estoque(azservicebus: func.ServiceBusMessage):
    logging.info(
        "Python ServiceBus Queue trigger processed a message: %s",
        azservicebus.get_body().decode("utf-8"),
    )
