from database.select_queries import Queries
from parser import TextParser

class FunctionsRouter():
    def __init__(self, q: Queries, tp: TextParser):
        self.func_by_ind = {
            0: q.select_gdp_sum,
            1: q.select_cars_by_country,
            2: q.select_area_sum,
            3: q.select_country_by_horsepower,
            4: q.select_currency
        }  #weird but it is describing program logic

        self.func_args_by_ind = {
            0: tp.first_question_parser,
            1: tp.second_question_parser,
            2: tp.third_question_parser,
            3: tp.fourth_question_parser,
            4: tp.fifth_question_parser
        }  #weird but it is describing program logic

        self.q = q
        self.tp = tp

    def get_right_function(self, text):
        func_ind = self.tp.question_identifier(text)
        func_args = self.func_args_by_ind[func_ind](text)
        func = self.func_by_ind[func_ind]

        return func, func_args