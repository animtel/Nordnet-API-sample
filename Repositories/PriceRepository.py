import pymysql

from Helpers.MappingHelper import to_dynamic
from Helpers.SettingsHelper import settings


def import_from_socket(json_string):
    print(json_string)
    connection = pymysql.connect(host=settings['connectionInfo']['host'],
                                 user=settings['connectionInfo']['user'],
                                 password=settings['connectionInfo']['password'],
                                 db=settings['connectionInfo']['database'],
                                 charset=settings['connectionInfo']['charset'])

    try:
        pricingModel = to_dynamic(json_string).data

        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `PricingTable` (" \
                  "`i`," \
                  "`m`," \
                  "`ask`," \
                  "`ask_volume`," \
                  "`bid`," \
                  "`bid_volume`," \
                  "`close`," \
                  "`high`," \
                  "`last`," \
                  "`last_volume`," \
                  "`low`," \
                  "`open`," \
                  "`tick_timestamp`," \
                  "`trade_timestamp`," \
                  "`turnover`," \
                  "`turnover_volume`," \
                  "`vwap`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            print(sql)
            cursor.execute(sql, (
                pricingModel.i, pricingModel.m, pricingModel.ask, pricingModel.ask_volume,
                pricingModel.bid, pricingModel.bid, pricingModel.bid_volume,
                pricingModel.close, pricingModel.high, pricingModel.last, pricingModel.last_volume, pricingModel.low,
                pricingModel.open, pricingModel.tick_timestamp,
                pricingModel.trade_timestamp, pricingModel.turnover, pricingModel.turnover_volume, pricingModel.vwap))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()
