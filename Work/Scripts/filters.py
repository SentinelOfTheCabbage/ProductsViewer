import pandas as pd
from Work.Scripts.db_controller import MainTableController
from Work.Scripts.interactors import ListMainTableInteractor


class FilterColumns:
    def filter(self, list_, m_table):
        frame: pd.DataFrame = MainTableController().get_data_frame()
        n = len(frame.columns)

        for i in frame.columns:
            if not (i in list_):
                del(frame[i])
        # print(frame)
        self.open(frame, m_table)

    def open(self, frame: pd.DataFrame, m_table):
        if frame is not None:
            m_table.before_content(ListMainTableInteractor().tolist(frame)
                                   [:100])
