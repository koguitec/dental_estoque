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
