from abc import ABC, abstractmethod

from Work.Scripts.src.controller.key_words import Expression
from Work.Scripts.src.model.repository.DB_constants import TableName


class ICommand(ABC):
    _table_name: TableName = None

    def set_table_name(self, table_name: TableName):
        self._table_name = table_name

    def get_table_name(self):
        return self._table_name

    @abstractmethod
    def get_data(self):
        pass


class ConditionProvider:
    _conditions = {}

    def add_condition(self, conditions: Expression):
        self._conditions[conditions.field] = conditions

    def set_conditions(self, conditions: list):
        self._conditions = conditions

    def remove_condition(self, conditions: Expression):
        self._conditions.pop(conditions.field, None)

    def get_conditions(self):
        return self._conditions


class CommandSelect(ICommand, ConditionProvider):
    _columns = []

    def add_column(self, column: str):
        self._columns.append(column)

    def remove_column(self, column: str):
        self._columns.remove(column)

    def set_columns(self, columns: list):
        self._columns = columns

    def get_columns(self):
        return self._columns

    def get_data(self):
        pass


class CommandInsert(ICommand):
    _row = []

    def add_row(self, row: dict):
        self._row = row.values()

    def get_row(self):
        return self._row

    def get_data(self):
        pass


class CommandUpdate(ICommand, ConditionProvider):
    _values = {}

    def update_values(self, values: dict):
        self._values = values

    def get_values(self):
        return self._values

    def get_data(self):
        pass


class CommandDelete(ICommand, ConditionProvider):
    def get_data(self):
        pass
