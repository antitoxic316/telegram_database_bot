class TextParser:
    def __init__(self):
        self.question_starts = [
            "Какой",
            "Какие автомобили",
            "Какова",
            "Какие страны",
            "Какая"
        ]

    def question_identifier(self, text):
        for  ind, start in enumerate(self.question_starts):
            if start in text:
                return ind
        raise ValueError("There is something wrong with the start of your question")

    def first_question_parser(self, question):
        splited_str = question.split(" ")
        splited_model = splited_str[10:]
        model_name = " ".join(splited_model)

        return model_name

    def second_question_parser(self, question):
        splited_str = question.split(" ")
        splited_country = splited_str[7:]
        country_name = " ".join(splited_country)

        return country_name

    def third_question_parser(self, question):
        cylinders = 0

        for ch in question:
            if ch.isdigit():
                cylinders = int(ch)
                break

        if not cylinders: raise ValueError("value for cylinders is wrong")

        return cylinders

    def fourth_question_parser(self, question):
        comparsion_sign = ""
        horsepower_num = ""

        if "более" in question:
            comparsion_sign = ">"
        elif "менее" in question:
            comparsion_sign = "<"
        else:
            raise ValueError("mistake in comparsion word")

        for i in range(0, len(question)):
            while question[i].isdigit():
                horsepower_num += question[i]
                i += 1
            if horsepower_num != "":
                break
        
        if horsepower_num == "":
            raise ValueError("wrong horsepower number")

        return comparsion_sign, horsepower_num
    
    def fifth_question_parser(self, question):
        key_word = ""
        aggregation_func = ""

        if "тяжелый" in question:
            key_word = "weight"
        elif "быстрый" in question:
            key_word = "acceleration"
        else:
            raise ValueError("mistake in characteristic word")

        if "дешевую" in question:
            aggregation_func = "min"
        elif "дорогую" in question:
            aggregation_func = "max"
        else:
            raise ValueError("mistake at currency comparsion")

        return key_word, aggregation_func


if __name__ == "__main__":
    question = "Какая из стран, которая входит в континент стран, выпускающих самый тяжелый/быстрый автомобиль имеют самую дешевую/дорогую валюту."

    tp = TextParser()

    print(tp.question_identifier(question))
    print(tp.fifth_question_parser(question))