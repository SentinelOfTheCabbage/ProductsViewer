"""docstring_peryatin
Отключены следующие ошибки pylint:
    R0903 - Ошибка количества методов в классе
"""
# pylint: disable=R0903
class Event:
    """
    Событие при редактировании БД

    Автор: Перятин Виталий
    """
    error: int = 0
    text: str = ""
    data: object = None
