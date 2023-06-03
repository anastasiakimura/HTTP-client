import unittest
from threading import Thread

from main import Main


def run_and_close_main(main: 'Main'):
    main.run()


class TestMain(unittest.TestCase):
    def test_main_func(self):
        main = Main()
        main_thread = Thread(
            target=run_and_close_main,
            args=[main]
        )

        main_thread.daemon = True
        main_thread.start()

        main.finish()

        assert True
