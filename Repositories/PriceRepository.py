import pymysql

from Helpers.MappingHelper import to_dynamic
from Helpers.SettingsHelper import settings

connection = pymysql.connect(host=settings['connectionInfo']['host'],
                                     user=settings['connectionInfo']['user'],
                                     password=settings['connectionInfo']['password'],
                                     db=settings['connectionInfo']['database'],
                                     charset=settings['connectionInfo']['charset'])

def import_from_socket(json_string):
    print('IMPORTED')
    print(json_string)
    try:
        with connection.cursor() as cursor:
            # sql = """CREATE TABLE `test` (
            #         `id` int(11) NOT NULL AUTO_INCREMENT,
            #         `email` varchar(500) COLLATE utf8_bin NOT NULL,
            #         `password` varchar(500) COLLATE utf8_bin NOT NULL,
            #         PRIMARY KEY (`id`)
            #         ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
            #         AUTO_INCREMENT=1 ;
            #         """
            # cursor.execute(sql)

            # Create a new record
            sql = "INSERT INTO `test` (`email`, `password`) VALUES (%s, %s)"
            cursor.execute(sql, (to_dynamic(json_string).type, 'very-secret'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `email`, `password` FROM `test` WHERE `password`=%s"
            cursor.execute(sql, ('very-secret',))
            result = cursor.fetchone()
            print(result)
    finally:
        #connection.close()
        print('INSERTED!')