import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='animtel',
                             password='w2e3r4T5',
                             db='menagerie',
                             charset='utf8mb4')

try:
    with connection.cursor() as cursor:
        # sql = """CREATE TABLE `users` (
        #         `id` int(11) NOT NULL AUTO_INCREMENT,
        #         `email` varchar(255) COLLATE utf8_bin NOT NULL,
        #         `password` varchar(255) COLLATE utf8_bin NOT NULL,
        #         PRIMARY KEY (`id`)
        #         ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
        #         AUTO_INCREMENT=1 ;
        #         """
        # cursor.execute(sql)

        # Create a new record
        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `email`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
