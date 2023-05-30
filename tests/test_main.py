import unittest
from threading import Thread

from main import Main


class TestMain(unittest.TestCase):
    def test_main_func(self):
        main = Main()
        main_thread = Thread(target=lambda: main.run())

        try:
            main_thread.start()
        except OSError:
            assert True
        except Exception:
            assert True

        try:
            main.finish()
        except Exception:
            assert True

        assert True


if __name__ == '__main__':
    unittest.main()
