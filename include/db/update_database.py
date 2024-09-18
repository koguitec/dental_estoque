import os
import logging

from pyodbc import connect

logger = logging.getLogger(__name__)


sql_query = """
    DECLARE IDProduto INT;
    SET @IDProduto = (SELECT IDProduto From Produto WHERE CodigoERP = ?);


    UPDATE Estoque 
    SET 
        SaldoTotal = ?,
        CustoProduto = ?,
        DtAlteracao = dbo.getdate2(),
    WHERE
        CodigoFilial = ? AND IDProduto = @IDProduto
"""


def update_database(payload: list[dict]) -> None:
    """Update stock levels in the database.

    Args:
        payload (list[tuple]): List of tuples containing stock data.
    """
    connection_string = os.environ["DB_CONN_STR"]

    try:
        conn = connect(connection_string)
        cursor = conn.cursor()
        cursor.fast_executemany = True

        # Execute the SQL query with the payload
        cursor.executemany(sql_query, payload)

        conn.commit()
        logger.info("Datatbase updated successfully.")
    except Exception as e:
        logger.error(f"Error updating database: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
