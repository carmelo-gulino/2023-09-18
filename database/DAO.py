from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def get_all_countries():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct gr.Country from go_retailers gr order by gr.Country """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row['Country'])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_nodes(country):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select * from go_retailers gr where gr.Country = %s"""
        cursor.execute(query, (country,))
        result = []
        for row in cursor:
            result.append(Retailer(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_peso(r1_code, r2_code, year):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select count(distinct gds2.Product_number) peso
                    from go_daily_sales gds , go_daily_sales gds2 
                    where gds.Retailer_code = %s and gds2.Retailer_code = %s 
                    and year (gds2.`Date`) = %s and year (gds2.`Date`) = year (gds.`Date`)
                    and gds2.Product_number = gds.Product_number"""
        cursor.execute(query, (r1_code, r2_code, year))
        result = None
        for row in cursor:
            result = row['peso']
        cursor.close()
        cnx.close()
        return result

