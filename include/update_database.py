


def ordered_items(payload: list[dict]) -> list[tuple]:
    """Função de ordenação dos campos para atualização de estoque.

    Args:
        payload (list[dict]): Example:
        [
            {"codigoFilial": "0", "codigoERP": "0", "saldo": 0, "custoProduto": 0},
            {"codigoFilial": "0", "codigoERP": "0", "saldo": 0, "custoProduto": 0},
            {"codigoFilial": "0", "codigoERP": "0", "saldo": 0, "custoProduto": 0},
            {"codigoFilial": "0", "codigoERP": "0", "saldo": 0, "custoProduto": 0},
        ]

    Returns:
        list[tuple]: Lista de tuplas com campos ordenador para inserção no banco
        de dados.
    """

    return [
        (item["codigoFilial"], item["codigoERP"], item["saldo"], item["custoProduto"])
        for item in payload
    ]



