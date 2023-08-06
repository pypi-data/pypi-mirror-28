import six

from datetime import datetime


class ResultSets(object):

    def __init__(self):
        self.foo = ''

    def selector(self, output):
        if isinstance(output, datetime):
            return self.parseDatetime(output)
        else:
            return output

    def formatter(self, output):
        if isinstance(output, list):
            return [self.formatter(item) for item in output]
        elif isinstance(output, dict):
            return {key: self.formatter(value) for key, value in six.iteritems(output)}
        else:
            return self.selector(output)

    def parseDatetime(self, output):
        return output.isoformat()
