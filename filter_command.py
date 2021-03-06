import sublime
import sublime_plugin

from .fin.fin import Transactions
from .fin.fin import Transaction
from .fin.fin import ParseError
from .fin.fin import query as fquery
from .fin.fin import currency


currency.setup_cache('currency.json')


class FinFilterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.query_from_input()

    def query_from_input(self):
        self.view.window().show_input_panel(
            'query', '',
            on_done=self.filter_and_sum,
            on_change=self.filter,
            on_cancel=self.unfold_all
        )

    def filter_and_sum(self, query):
        self.filter(query)
        content = self.view.substr(sublime.Region(0, self.view.size()))
        try:
            transactions = Transactions(content).filter(query)
        except ParseError:
            return
        self.show_sum(transactions)

    def filter(self, query):
        self.unfold_all()
        try:
            query = fquery(query)
        except ParseError:
            return
        content = self.view.substr(sublime.Region(0, self.view.size()))
        lines_to_fold = self.find_lines_to_fold(content, query)
        self.fold_lines(lines_to_fold)

    def find_lines_to_fold(self, content, query):
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if not line:
                yield i
                continue
            if line.startswith('#'):
                yield i
                continue
            if not query(Transaction(line)):
                yield i

    def fold_lines(self, indices):
        regions_to_fold = self.find_regions_to_fold(indices)
        for region in self.coalesce_neighboring_regions(regions_to_fold):
            self.view.fold(region)

    def find_regions_to_fold(self, indices):
        for index in indices:
            yield self.view.line(self.view.text_point(index, 0))

    def coalesce_neighboring_regions(self, regions):
        prev_region = None
        for region in regions:
            if prev_region:
                if prev_region.b == region.a - 1:
                    prev_region = sublime.Region(prev_region.a, region.b)
                else:
                    yield prev_region
                    prev_region = region
            else:
                prev_region = region
            # yield region
        if prev_region: yield prev_region

    def unfold_all(self):
        self.view.unfold(sublime.Region(0, self.view.size()))

    def show_sum(self, transactions):
        total = transactions.sum()
        lines = [str(total)]
        currencies = total.currencies()
        if len(currencies) > 1:
            for currency in currencies:
                lines.append('= ' + str(total.convert(currency)))

        self.view.window().show_quick_panel(
            lines, lambda _: None
        )
