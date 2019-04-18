from threading import Thread


def threading_start(func, args):
    if args is None:
        proc = Thread(target=func)
        proc.start()
    else:
        proc = Thread(target=func, args=args)
        proc.start()
