import unittest
import io
from unittest.mock import patch
from tutorial.list.example_list_001.example_list_001 import ListManager, main

class TestListManager(unittest.TestCase):
    def test_init(self):
        self.assertEqual(ListManager().data, [])
        self.assertEqual(ListManager(["a", "b"]).data, ["a", "b"])

    def test_add(self):
        manager = ListManager(["a"])
        self.assertEqual(manager.add("b"), ["a", "b"])

    def test_remove(self):
        manager = ListManager(["a", "b", "c"])
        self.assertEqual(manager.remove("b"), ["a", "c"])
        # Test removing item not in list to ensure no exception is raised
        self.assertEqual(manager.remove("x"), ["a", "c"])

    def test_sort(self):
        manager = ListManager(["z", "a", "k"])
        self.assertEqual(manager.sort(), ["a", "k", "z"])

    def test_reverse(self):
        manager = ListManager(["a", "b", "c"])
        self.assertEqual(manager.reverse(), ["c", "b", "a"])

    def test_pop(self):
        manager = ListManager(["a", "b"])
        self.assertEqual(manager.pop(), "b")
        self.assertEqual(manager.data, ["a"])
        
        # Test popping from empty list
        empty_manager = ListManager()
        self.assertIsNone(empty_manager.pop())

    def test_clear(self):
        manager = ListManager(["a", "b"])
        self.assertEqual(manager.clear(), [])

class TestCLI(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['list_ops.py', '--data', 'x', 'y', '--add', 'z'])
    def test_cli_add(self, mock_stdout):
        main()
        self.assertIn("Result: ['x', 'y', 'z']", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['list_ops.py', '--data', 'x', 'y', '--remove', 'x'])
    def test_cli_remove(self, mock_stdout):
        main()
        self.assertIn("Result: ['y']", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['list_ops.py', '--data', 'b', 'a', '--sort'])
    def test_cli_sort(self, mock_stdout):
        main()
        self.assertIn("Result: ['a', 'b']", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['list_ops.py', '--data', 'a', 'b', '--reverse'])
    def test_cli_reverse(self, mock_stdout):
        main()
        self.assertIn("Result: ['b', 'a']", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['list_ops.py', '--data', 'a', 'b', '--pop'])
    def test_cli_pop(self, mock_stdout):
        main()
        self.assertIn("Popped: b, Remaining: ['a']", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['list_ops.py', '--data', 'a', 'b', '--clear'])
    def test_cli_clear(self, mock_stdout):
        main()
        self.assertIn("Result: []", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['list_ops.py', '--data', 'a', 'b'])
    def test_cli_default(self, mock_stdout):
        main()
        self.assertIn("Current List: ['a', 'b']", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_cli_single_string_args(self, mock_stdout):
        main(["--data Nick Filippos Dimitra --sort"])
        self.assertIn("Result: ['Dimitra', 'Filippos', 'Nick']", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('sys.argv', ['example_list_001.py', '--data Nick Filippos Dimitra --sort'])
    def test_cli_sys_argv_single_string(self, mock_stdout):
        main()
        self.assertIn("Result: ['Dimitra', 'Filippos', 'Nick']", mock_stdout.getvalue())

if __name__ == "__main__":
    unittest.main()
