'''URL = "https://api.telegram.org/bot1487290287:AAGx6gtPv0G6ROiQ6jNQE0EZ2QsOb9ZDMcU/"
MyURL = "https://example.com/hook"

api = requests.Session()
application = tornado.web.Application([(r"/", Handler), ])

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_term_handler)'''
