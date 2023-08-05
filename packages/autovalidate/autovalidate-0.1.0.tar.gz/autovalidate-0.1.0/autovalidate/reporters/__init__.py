import sys

from autovalidate.utils import indent


class Reporter(object):
    def __init__(self, out):
        self.out = out
        self.valid_results = []
        self.invalid_results = []

    @property
    def valid_count(self):
        return len(self.valid_results)

    @property
    def invalid_count(self):
        return len(self.invalid_results)

    @property
    def exit_code(self):
        return 0 if self.invalid_count == 0 else 1

    def record(self, result):
        if result.valid:
            self.valid_results.append(result)
        else:
            self.invalid_results.append(result)

        self.report(result)

    def report(self, result):
        raise NotImplementedError

    def summarize(self):
        for result in self.invalid_results:
            self.out.write('\n%s:\n%s\n' % (result.path,
                                            indent(result.message)))
        self.out.write('\n%d valid, %d invalid\n' % (self.valid_count,
                                                     self.invalid_count))


class DotReporter(Reporter):
    def report(self, result):
        self.out.write('.' if result.valid else 'F')


class ListReporter(Reporter):
    def report(self, result):
        if result.valid:
            self.out.write(u'\033[92m\u2713\033[0m %s\n' % result.path)
        else:
            self.out.write(u'\033[91m\u2717 %s\033[0m\n' % result.path)

reporter_classes = {
    'dot': DotReporter,
    'list': ListReporter
}


def get_reporter(name='dot', out=None):
    if name not in reporter_classes:
        raise ValueError('unknown reporter: "%s"' % name)
    if out is None:
        out = sys.stdout
    return reporter_classes[name](out)
