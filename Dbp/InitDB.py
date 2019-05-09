from Dbp.InitPricing import init_pricing


def initdb():
    try:
        init_pricing()
    except Exception as ex:
        print('Db already initialized', ex)
