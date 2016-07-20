import sys
import sublime
import unittest

FinanseFilterCommand = sys.modules["Finanse.filter_commands"].FinanseFilterCommand

transactions = """
2016-01-01 a 1zł
2016-01-01 b 1zł
2016-01-01 b 1zł
2016-01-01 a 1zł
2016-01-01 b 1zł
""".strip()


class FilterCommandTestCase(unittest.TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()
        self.command = FinanseFilterCommand(self.view)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def set_text(self, string):
        self.view.run_command("insert", {"characters": string})

    def test_filter(self):
        folded = []
        def fold_mock(region):
            folded.append(region)

        self.view.fold = fold_mock
        self.set_text(transactions)
        self.command.filter('a')
        self.assertEqual(
            folded, [
                sublime.Region(17, 50),
                sublime.Region(68, 84)
            ]
        )
        folded = []
        self.command.filter('b')
        self.assertEqual(
            folded, [
                sublime.Region(0, 16),
                sublime.Region(51, 67)
            ]
        )

    def test_find_lines_to_fold(self):
        lines_to_fold = self.command.find_lines_to_fold(
            transactions, lambda t: 'a' in t.tags
        )
        self.assertEqual(list(lines_to_fold), [1, 2, 4])

    def test_coalesce_neighboring_regions(self):
        regions = self.command.coalesce_neighboring_regions([
            sublime.Region(0, 10),
            sublime.Region(11, 20),
            sublime.Region(25, 26),
            sublime.Region(30, 40),
            sublime.Region(41, 50),
        ])
        self.assertEqual(
            list(regions),
            [
                sublime.Region(0, 20),
                sublime.Region(25, 26),
                sublime.Region(30, 50)
            ]
        )
