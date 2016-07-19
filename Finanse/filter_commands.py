from . import finanse
import sublime
import sublime_plugin


class FinanseFilterCommand(sublime_plugin.TextCommand):
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
        transactions = finanse.Transactions(content).filter(query)
        self.view.window().show_quick_panel(
            [str(transactions.sum())], lambda _: None
        )

    def filter(self, query):
        self.unfold_all()
        query = finanse.query(query)
        content = self.view.substr(sublime.Region(0, self.view.size()))
        lines_to_fold = self.find_lines_to_fold(content, query)
        self.fold_lines(lines_to_fold)

    def find_lines_to_fold(self, content, query):
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if not query(finanse.Transaction(line)):
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
            yield region
        if prev_region: yield prev_region

    def unfold_all(self):
        self.view.unfold(sublime.Region(0, self.view.size()))
