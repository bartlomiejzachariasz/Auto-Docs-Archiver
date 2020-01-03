import xes

from random import randrange
from datetime import timedelta, datetime


class XesGenerator:

    def generate(self, traces_json):
        traces = []

        d1 = datetime.strptime('1/1/2010 1:30 PM', '%m/%d/%Y %I:%M %p')
        d2 = datetime.strptime('12/1/2010 4:50 AM', '%m/%d/%Y %I:%M %p')

        for trace in traces_json:
            if trace["date"] is None:
                trace["date"] = self.random_date(d1, d2)

        traces_pairs = sorted(traces_json, key=lambda k: k['date'])

        for entry in traces_pairs:
            trace = {
                "concept:name": entry["title"]
            }

            traces.append([trace])

        log = xes.Log()

        t = xes.Trace()

        for trace in traces:

            for event in trace:
                e = xes.Event()
                e.attributes = [
                    xes.Attribute(type="string", key="concept:name", value=event["concept:name"])
                ]
                t.add_event(e)
            log.add_trace(t)
        log.classifiers = [
            xes.Classifier(name="concept:name", keys="concept:name")
        ]

        open("../output/example.xes", "w").write(str(log))
        return str(log)

    def random_date(self, start, end):
        """
        This function will return a random datetime between two datetime
        objects.
        """
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = randrange(int_delta)
        return start + timedelta(seconds=random_second)
