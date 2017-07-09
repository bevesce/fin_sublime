import sublime
import sublime_plugin

from .finanse.finanse import Transactions
from .finanse.finanse import Transaction
from .finanse.finanse import ParseError
from .finanse.finanse import query as fquery
from .finanse.finanse import currency


currency.setup_cache('currency.json')


class FinanseMergeCommand(sublime_plugin.TextCommand):
    merge_key = None

    def run(self, edit):
        merge_key = self.merge_key
        new_line = str(Transactions(self.collect_selections()).merge(merge_key))
        self.remove_selections_additional_selections(edit)
        self.replace_first_selection(edit, new_line)

    def collect_selections(self):
        collected = []
        for region in self.view.sel():
            full_line_region = self.view.full_line(region)
            collected.append(
                self.view.substr(full_line_region).rstrip()
            )
        return '\n'.join(collected)

    def replace_first_selection(self, edit, new_content):
        full_line_region = self.view.full_line(self.view.sel()[0])
        self.view.replace(edit, full_line_region, new_content + '\n')

    def remove_selections_additional_selections(self, edit):
        for region in list(self.view.sel())[1:][::-1]:
            full_line_region = self.view.full_line(region)
            self.view.replace(edit, full_line_region, '')
        first = self.view.sel()[0]
        self.view.sel().clear()
        self.view.sel().add(first)


class FinanseMergeWithSameTagsCommand(FinanseMergeCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.merge_key = lambda t: ':'.join(t.money.currencies()) + ', '.join(sorted(t.tags.keys()))
