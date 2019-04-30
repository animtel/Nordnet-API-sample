import pymysql

from Helpers.MappingHelper import to_dynamic
from Helpers.SettingsHelper import settings


def import_price_from_socket(json_string):
    # isPricingType = to_dynamic(json_string).type
    # if str(isPricingType) is not 'price':
    #     return

    connection = pymysql.connect(host=settings['connectionInfo']['host'],
                                 user=settings['connectionInfo']['user'],
                                 password=settings['connectionInfo']['password'],
                                 db=settings['connectionInfo']['database'],
                                 charset=settings['connectionInfo']['charset'])

    try:
        pricingModel = to_dynamic(json_string).data

        with connection.cursor() as cursor:

            sql = """SELECT JSON_OBJECT(
                      'i', i,
                      'm', m,
                      'ask', ask,
                      'ask_volume', ask_volume,
                      'bid', bid,
                      'bid_volume', bid_volume,
                      'close', close,
                      'high', high,
                      'last', last,
                      'last_volume', last_volume,
                      'low', low,
                      'open', open,
                      'tick_timestamp', tick_timestamp,
                      'trade_timestamp', trade_timestamp,
                      'turnover', turnover,
                      'turnover_volume', turnover_volume,
                      'vwap', vwap
                    )
                    FROM `PricingTable` WHERE i = {0} AND m = {1}""".format(pricingModel.i, pricingModel.m)
            cursor.execute(sql)
            test = to_dynamic(cursor.fetchall()[0][0])
            print('test')
            print(test)

            # # Create a new record
            # sql = "INSERT INTO `PricingTable` (" \
            #       "`i`," \
            #       "`m`," \
            #       "`ask`," \
            #       "`ask_volume`," \
            #       "`bid`," \
            #       "`bid_volume`," \
            #       "`close`," \
            #       "`high`," \
            #       "`last`," \
            #       "`last_volume`," \
            #       "`low`," \
            #       "`open`," \
            #       "`tick_timestamp`," \
            #       "`trade_timestamp`," \
            #       "`turnover`," \
            #       "`turnover_volume`," \
            #       "`vwap`) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}')"\
            #     .format(pricingModel.i, pricingModel.m, pricingModel.ask, pricingModel.ask_volume,
            #     pricingModel.bid, pricingModel.bid, pricingModel.bid_volume,
            #     pricingModel.close, pricingModel.high, pricingModel.last, pricingModel.last_volume, pricingModel.low,
            #     pricingModel.open, pricingModel.tick_timestamp,
            #     pricingModel.trade_timestamp, pricingModel.turnover, pricingModel.turnover_volume, pricingModel.vwap)
            #
            # print(sql)
            cursor.execute(sql)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()
