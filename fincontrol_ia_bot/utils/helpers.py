import os

def get_env_variable(var_name: str, default: str = None) -> str:
    """
    Recupera uma variável de ambiente ou retorna um valor padrão.
    """
    return os.environ.get(var_name, default)

def format_currency(value: float) -> str:
    """
    Exemplo de função utilitária: formata um float para Moeda (R$).
    """
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
