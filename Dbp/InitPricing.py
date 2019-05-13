import pymysql
from Helpers.SettingsHelper import settings

def init_pricing():
    try:
        connection = pymysql.connect(host=settings['connectionInfo']['host'],
                                     port=int(settings['connectionInfo']['port']),
                                     user=settings['connectionInfo']['user'],
                                     password=settings['connectionInfo']['password'],
                                     db=settings['connectionInfo']['database'],
                                     charset=settings['connectionInfo']['charset'])
        with connection.cursor() as cursor:
            sql = """CREATE TABLE `PricingTable` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `i` varchar(1024) COLLATE utf8_bin NOT NULL,
                        `m` bigint NOT NULL,
                        `ask` decimal,
            			`ask_volume` int,
                        `bid` decimal,
                        `bid_volume` int,
                        `close` decimal,
                        `high` decimal,
                        `last` decimal,
                        `last_volume` int,
                        `low` decimal,
                        `open` decimal,
                        `tick_timestamp` bigint,
                        `trade_timestamp` bigint,
                        `turnover` bigint,
                        `turnover_volume` decimal,
                        `vwap` decimal,
                         PRIMARY KEY (`id`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
                        AUTO_INCREMENT=1 ;
                    """
            cursor.execute(sql)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()
