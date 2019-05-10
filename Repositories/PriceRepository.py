import json
import logging

import pymysql

from Helpers.MappingHelper import to_dynamic, update_exist_props
from Helpers.SettingsHelper import settings


def import_price_from_socket(json_string):
    isPricingType = to_dynamic(json_string).type != 'price'
    print(json_string)
    if isPricingType:
        return

    connection = pymysql.connect(host=settings['connectionInfo']['host'],
                                 port=int(settings['connectionInfo']['port']),
                                 user=settings['connectionInfo']['user'],
                                 password=settings['connectionInfo']['password'],
                                 db=settings['connectionInfo']['database'],
                                 charset=settings['connectionInfo']['charset'])

    try:
        logging.info(">> Pricing updated")
        logging.info(json.dumps(json_string, indent=4, sort_keys=True))

        pricingModel = to_dynamic(json_string).data

        with connection.cursor() as cursor:

            selected_pricing = get_pricing_by_i_m(pricingModel.i, pricingModel.m, 1)
            if selected_pricing != None:
                fullObj = to_dynamic(selected_pricing[0][0])
                insertionObject = update_exist_props(fullObj, pricingModel)
            else:
                insertionObject = pricingModel
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
                  "`vwap`) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}')" \
                .format(insertionObject.i, insertionObject.m, insertionObject.ask, insertionObject.ask_volume,
                        insertionObject.bid, insertionObject.bid_volume,
                        insertionObject.close, insertionObject.high, insertionObject.last, insertionObject.last_volume,
                        insertionObject.low,
                        insertionObject.open, insertionObject.tick_timestamp,
                        insertionObject.trade_timestamp, insertionObject.turnover, insertionObject.turnover_volume,
                        insertionObject.vwap)

            cursor.execute(sql)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
    finally:
        connection.close()


def get_pricing():
    connection = pymysql.connect(host=settings['connectionInfo']['host'],
                                 port=int(settings['connectionInfo']['port']),
                                 user=settings['connectionInfo']['user'],
                                 password=settings['connectionInfo']['password'],
                                 db=settings['connectionInfo']['database'],
                                 charset=settings['connectionInfo']['charset'])

    result = None
    try:
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
                    FROM `PricingTable`"""
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        connection.close()

    return result


def get_pricing_by_i_m(i, m, amount):
    connection = pymysql.connect(host=settings['connectionInfo']['host'],
                                 port=int(settings['connectionInfo']['port']),
                                 user=settings['connectionInfo']['user'],
                                 password=settings['connectionInfo']['password'],
                                 db=settings['connectionInfo']['database'],
                                 charset=settings['connectionInfo']['charset'])

    result = None
    try:
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
                    FROM `PricingTable`
                    WHERE i = {0} AND m = {1}
                    ORDER BY id DESC LIMIT {2}""".format(i, m, amount)
            cursor.execute(sql)
            result = cursor.fetchall()
    finally:
        connection.close()

    return result
