class Queries:
    def __init__(self, db_connection):
        self.conn = db_connection

    def select_gdp_sum(self, car_name: str):
        sql = f"with all_cars_cte as ( \
                select * from countries c \
                inner join continents c2 on c.name = c2.country \
                right join cars c3 on c2.continent = c3.new_continent \
                where c3.car = '{car_name}' \
            ), unique_countries_cte as ( \
                select distinct country, gdp from all_cars_cte \
            ) \
            select sum(gdp) from unique_countries_cte"

        with self.conn.cursor() as curs:
            curs.execute(sql)
            result = str(curs.fetchall()[0][0])
        return result


    def select_cars_by_country(self, country_name):
        sql = f"select distinct car from countries c \
                inner join continents c2 on c.name = c2.country \
                right join cars c3 on c2.continent = c3.new_continent \
                where c2.country = '{country_name}'"

        with self.conn.cursor() as curs:
            curs.execute(sql)
            result = str(curs.fetchall())[2:-2].replace("), (", " ")

        return result

    def select_area_sum(self, cylinders_num):
        sql = f"with all_countries_cte as ( \
                    select * from countries c \
                    inner join continents c2 on c.name = c2.country \
                    right join cars c3 on c2.continent = c3.new_continent \
                    where c3.cylinders = {cylinders_num} \
                ), unique_countries_cte as ( \
                    select distinct country, area from all_countries_cte \
                ) \
                select sum(area) from unique_countries_cte"

        with self.conn.cursor() as curs:
            curs.execute(sql)
            result = str(curs.fetchall()[0][0]) + "(sq km)"

        return result

    def select_country_by_horsepower(self, comparsion_sign, horsepower):
        sql = f"select distinct c.name from countries c \
                inner join continents c2 on c.name = c2.country \
                right join cars c3 on c2.continent = c3.new_continent \
                where c3.horsepower {comparsion_sign} {horsepower}"

        with self.conn.cursor() as curs:
            curs.execute(sql)
            result = str(curs.fetchall())[2:-2].replace("), (", " ")

        return result

    def select_currency(self, by_what: str, aggregation_func: bool):
        sql = f"with joined_tables_cte as ( \
                    select * from countries c \
                    inner join continents c2 on c.name = c2.country \
                    right join cars c3 on c2.continent = c3.new_continent \
                    inner join currency_codes cc on cc.country = c2.country \
                    inner join currency_rates cr on cr.currency_code = cc.currency_code \
                    where c3.{by_what} = (select max({by_what}) from cars) \
                ) \
                select \"name\" from joined_tables_cte \
                where exchange_rate = (select {aggregation_func}(exchange_rate) from joined_tables_cte)"
        with self.conn.cursor() as curs:
            curs.execute(sql)
            result = str(curs.fetchall()[0][0])

        return result