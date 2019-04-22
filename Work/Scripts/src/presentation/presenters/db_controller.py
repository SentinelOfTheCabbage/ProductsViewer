import copy


from Work.Scripts.src.presentation.presenters.commands import CommandSelect, CommandInsert, \
    CommandUpdate, CommandDelete
from Work.Scripts.src.presentation.presenters.db_event import Event
from Work.Scripts.src.presentation.presenters.errors import EditDbError
from Work.Scripts.src.presentation.presenters.factory import ProdDbFactory
from Work.Scripts.src.domain.interactors import ReportsInteractor, \
    MainTableInteractor
from Work.Scripts.src.model.repository.UI_table_constants import \
    ProductColumns, TableNameUI
from Work.Scripts.src.presentation.views.app import App

db_factory = ProdDbFactory()

EMPTY_EXPRS = "Не заполнены условия"
EMPTY_COLS = "Не выбраны колонки"
EMPTY_VALS = "Не заполнены значения"


class MainTableController:
    states = App.getInstance().saved_states

    def __init__(self, save_curr_state=False):
        self.main_interactor = MainTableInteractor(
            db_factory.create_table_extractor())
        self.selector = CommandSelect(TableNameUI.PRODUCTS.value)
        if save_curr_state:
            self._save_state()

    def get_data_frame(self):
        return self.main_interactor.get_main_table()

    def get_columns_by_table(self, table):
        pass

    def select(self, column_choices: dict, expressions):
        columns = []

        def get_text():
            col_text = 'По столбцам: ' + ', '.join(columns)
            exprs = []
            for expr in expressions:
                field, op, val = expr.get_expression()
                exprs.append(str(field) + str(op) + str(val))
            if exprs:
                expr_text = '\nПо условиям: ' + '; '.join(exprs)
            else:
                expr_text = ''
            return 'Таблица отфильтрована\n' + col_text + expr_text

        for col, var in column_choices.items():
            if var.get():
                columns.append(col)

        is_full_exprs = True
        for expr in expressions:
            if expr.get_expression()[2] == '':
                is_full_exprs = False
                break

        if not columns:
            err = EditDbError.EMPTY_FIELDS.value
            return Event(err, EMPTY_COLS)
        elif not is_full_exprs:
            err = EditDbError.EMPTY_FIELDS.value
            return Event(err, EMPTY_EXPRS)
        else:
            self.selector = CommandSelect(TableNameUI.PRODUCTS.value)
            self.selector.set_columns(columns)
            self.selector.set_conditions(expressions)
            data = self.main_interactor.select(self.selector)
            self._save_state()
            return Event(0, get_text(), data)

    def insert(self, col_to_values: dict):

        def get_text(cut_row: list):
            return "В БД добавлена следующая строка... \n" + ", ".join(cut_row)

        is_full_row = True
        row = {}
        for col, val in col_to_values.items():
            if not val.get():
                is_full_row = False
            else:
                row[col] = val.get()

        if is_full_row:
            inserter = CommandInsert()
            inserter.add_row(row)
            row_list = self.main_interactor.insert(inserter)
            titled_row = dict(zip(ProductColumns.get_empty_row().keys(),
                                  row_list))
            cutted_row = [val for col, val in titled_row.items()
                          if col in list(self.selector.get_columns())]
            self._save_state()
            return Event(0, get_text(cutted_row), cutted_row)
        else:
            return Event(EditDbError.EMPTY_FIELDS.value, EMPTY_VALS)

    def update(self, set_frames: list, expressions: list):

        def get_text():
            return "Обновлены строки"

        values = {}
        updater = CommandUpdate()
        is_full_vals = True
        for set_frame in set_frames:
            col_to_val = set_frame.get_col_to_value()
            if list(col_to_val.values())[0] != '':
                values.update(set_frame.get_col_to_value())
            else:
                is_full_vals = False
                break

        if (not is_full_vals) or (not values):
            return Event(EditDbError.EMPTY_FIELDS.value, EMPTY_VALS)
        elif not expressions:
            return Event(EditDbError.EMPTY_FIELDS.value, EMPTY_EXPRS)
        else:
            updater.update_values(values)
            updater.set_conditions(expressions)
            data = self.main_interactor.update(updater)
            self._save_state()
            return Event(0, get_text(), data)

    def delete(self, expressions):

        def get_text():
            return "Удалены записи"

        is_full_exprs = True
        for expr in expressions:
            if expr.get_expression()[2] == '':
                is_full_exprs = False
                break

        if (expressions is None) or (not is_full_exprs) or (not expressions):
            return Event(EditDbError.EMPTY_FIELDS.value, EMPTY_EXPRS)
        else:
            deleter = CommandDelete()
            deleter.set_conditions(expressions)
            data = self.main_interactor.delete(deleter)
            self._save_state()
            return Event(0, get_text(), data)

    def get_vals_by_col(self, column):
        return self.main_interactor.get_vals_by_col(column)

    def _save_state(self):
        self.states.add((self.main_interactor.get_db_copy(),
                         copy.deepcopy(self.selector)))

    def prev_state(self):
        def get_text():
            return "Шаг назад"
        tuple_state = self.states.prev()
        if tuple_state is None:
            return Event(EditDbError.NO_SELECTOR.value, "")
        else:
            state, selector = tuple_state
            self.main_interactor.set_data(state)
            return Event(0, get_text(), self.main_interactor.select(selector))

    def next_state(self):
        def get_text():
            return "Шаг вперёд"

        tuple_state = self.states.next()
        if tuple_state is None:
            return Event(EditDbError.NO_SELECTOR.value, "")
        else:
            state, selector = tuple_state
            self.main_interactor.set_data(state)
            return Event(0, get_text(), self.main_interactor.select(selector))


class ReportsController:

    def __init__(self):
        self.reports_interactor = ReportsInteractor(
            db_factory.create_table_extractor())

    def get_products_groups(self):
        return self.reports_interactor.get_products_groups()

    def get_quality_categories(self):
        return self.reports_interactor.get_quality_list()

    def get_prices_by_group_and_quality(self, groups: list, quality: list):
        return self.reports_interactor.get_prices_by_group_and_quality(
            groups, quality)

    def get_products_by_group(self, group: str):
        return self.reports_interactor.get_products_by_group(group)

    def get_box_and_whisker_prices(self, product_group: str, qualities: list,
                                   products: list):
        return self.reports_interactor.get_box_and_whisker_prices(
            product_group, qualities, products)

    def get_prices_by_group(self, product_group: str, products: list):

        return self.reports_interactor.get_prices_by_group(product_group,
                                                           products)

    def get_spreading(self, product_group: str, date: str):
        return self.reports_interactor.get_spreading(product_group,
                                                     date)
