import azure.functions as func
import os
import json
import logging

from pyodbc import connect

logger = logging.getLogger(__name__)

app = func.FunctionApp()

sql_query = """
    DECLARE @IDProduto INT;
    SET @IDProduto = (SELECT IDProduto From Produto WHERE CodigoERP = ?);


    UPDATE Estoque 
    SET 
        SaldoTotal = ?,
        CustoProduto = ?,
        DtAlteracao = dbo.getdate2(),
    WHERE
        CodigoFilial = ? AND IDProduto = @IDProduto
"""


def update_database(payload: list[tuple]) -> None:
    """Update stock levels in the database.

    Args:
        payload (list[tuple]): List of tuples containing stock data.
    """
    logger.debug("Reading connection string.")
    connection_string = os.environ["DB_CONN_STR"]

    try:
        logger.info(f"Writing {len(payload)} entries to database...")
        conn = connect(connection_string)
        cursor = conn.cursor()
        cursor.fast_executemany = True

        # Execute the SQL query with the payload
        cursor.executemany(sql_query, payload)

        conn.commit()
        logger.info("Database updated successfully.")
    except Exception as e:
        logger.error(f"Error updating database: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def order_items(payload: list[dict]) -> list[tuple]:
    """Reorder payload items into a tuple format for database insertion.

    Args:
        payload (list[dict]): List of dictionaries with stock data.

    Returns:
        list[tuple]: Ordered tuples ready for database update.
    """
    return [
        (
            item["codigoERP"],
            item["saldo"],
            item["custoProduto"],
            item["codigoFilial"],
        )
        for item in payload
    ]


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

    # Parse the message body
    message = azservicebus.get_body().decode("utf-8")

    # Assuming the message body contains a list of items in JSON format
    try:
        payload = json.loads(message)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode the message body: {e}")
        return

    # Order the payment data
    ordered_data = order_items(payload)

    # Update the database
    try:
        update_database(ordered_data)
    except Exception as e:
        logger.error(f"Failed to update database: {e}")
