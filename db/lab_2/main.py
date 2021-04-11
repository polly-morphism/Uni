import csv
import psycopg2
from datetime import datetime, timedelta
from psycopg2.errors import lookup
import re
import os
import logging


class ZNO:
    def __init__(self):
        self.dbtable = "ZNO_TABLE"
        self.last_row = "LastRowTable"
        self.years = [2019, 2020]
        self.query = """select max(res.UkrBall100), res.TestYear, res.REGNAME from {} as res
        where res.mathTestStatus = 'Зараховано'
        group by res.TestYear, res.REGNAME
        """.format(
            self.dbtable
        )
        self.log = logging.getLogger(__name__)
        logging.basicConfig(
            filename="work_logs.log",
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s at row #%(lineno)d %(message)s",
            datefmt="%m-%d-%Y %H:%M:%S",
        )

    def create(self, conn, cursor):
        self.log.info("Creating table")

        with open("queries/CREATE_BUFFER_TABLE.sql") as create_file:
            row_table_create = create_file.read().format(table_name=self.last_row)

        with open("queries/CREATE_TABLE.sql") as create_file:
            create_table_query = create_file.read().format(table_name=self.dbtable)

        try:
            cursor.execute(create_table_query)
        except Exception as e:
            self.log.error("Table {}, {}".format(self.dbtable, e))

        try:
            cursor.execute(row_table_create)
            cursor.execute("INSERT INTO {} VALUES (0, 0, 0)".format(self.last_row))
        except Exception as e:
            self.log.error("{}".format(e))

        conn.commit()
        self.log.info("Tables created")

    def create_insertion(self, row, year):
        buf = [row[el].replace("'", "`").split(",")[0] for el in row]
        buf.append(year)
        insert_buf = "insert into {} values".format(self.dbtable) + str(tuple(buf))

        insert_query = re.sub(r"'null'", "null", insert_buf)
        return insert_query

    def get_query(self, cursor):
        """
        Варіант 1:
        Порівняти найкращий бал з Української мови та літератури у кожному
        регіоні у2020 та 2019 роках серед тих кому було зараховано тест
        """

        outputquery = "COPY ({}) TO STDOUT WITH CSV HEADER".format(self.query)

        with open("resultQuery.csv", "w") as f:
            cursor.copy_expert(outputquery, f)
        self.log.info("COPY TO CSV SUCCESSFUL")

    def get_run_t(self, cursor):
        try:
            cursor.execute("SELECT execute_time FROM {};".format(self.last_row))
            buf = cursor.fetchall()
            last_t = buf[0][0]
        except Exception as e:
            self.log.info("Cannot get data from {}: {}".format(self.last_row, e))
            last_t = None

        return timedelta(microseconds=last_t)

    def insertion(self, conn, cursor, csv_filename, year, last_row_number, start_time):
        previous_stack_time = start_time
        self.log.info("Inserting data from {}".format(csv_filename))
        with open(csv_filename, encoding="cp1251") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=";")

            i = 0
            for row in csv_reader:
                i += 1

                if i <= last_row_number:
                    continue
                try:
                    cursor.execute(self.create_insertion(row, year))
                except Exception as e:
                    self.log.error("Something went wrong details ->: {}".format(e))
                    conn.rollback()
                    return 1

                if i % 50 == 0:
                    now = datetime.now()
                    try:
                        cursor.execute(
                            "UPDATE {} SET row_num={}, year_file={}, ".format(
                                self.last_row, i, year
                            )
                            + "\n"
                            + "execute_time=execute_time+"
                            + "\n"
                            + "{};".format((now - previous_stack_time).microseconds)
                        )
                        conn.commit()
                        print(i)
                    except Exception as e:
                        self.log.error("Connection with db is broken: {}".format(e))
                        conn.rollback()
                        return 1
                    previous_stack_time = now

            conn.commit()

        self.log.info("Inserting from {} is finished".format(csv_filename))

    def run(self):
        start_time = datetime.now()
        self.log.info("Start time {}".format(start_time))
        conn = psycopg2.connect(
            dbname=os.environ.get("db_name"),
            user=os.environ.get("db_user"),
            password=os.environ.get("db_password"),
            host=os.environ.get("db_url"),
        )
        cursor = conn.cursor()
        self.create(conn, cursor)

        try:
            cursor.execute("SELECT * FROM {};".format(self.last_row))
            buf = cursor.fetchall()
            file_year = buf[0][0]
            row_number = buf[0][1]
        except Exception as e:
            self.log.warning("Cannot get data from {}: {}".format(self.last_row, e))
            file_year = self.years[0]
            row_number = 0

        conn.commit()
        self.log.info(
            "Starting inserting from {} row from file for {} year".format(
                row_number, file_year
            )
        )
        if file_year:
            index = self.years.index(file_year)
            for year in self.years[index:]:
                self.insertion(
                    conn,
                    cursor,
                    "Odata{}File.csv".format(year),
                    year,
                    row_number,
                    start_time,
                )
                row_number = 0
        else:
            for year in self.years:
                self.insertion(
                    conn,
                    cursor,
                    "Odata{}File.csv".format(year),
                    year,
                    row_number,
                    start_time,
                )
                row_number = 0

        self.get_query(cursor)
        inserting_time = self.get_run_t(cursor)
        end_time = datetime.now()
        self.log.info("End time {}".format(end_time))
        self.log.info("Inserting executing time {}".format(inserting_time))
        cursor.close()
        conn.close()
        self.log.info("Program is finished")


if __name__ == "__main__":
    zno = ZNO()
    zno.run()
