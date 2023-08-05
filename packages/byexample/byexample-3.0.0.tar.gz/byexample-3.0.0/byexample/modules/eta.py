from byexample.concern import Concern
import time

class EstimateTime(Concern):
    def __init__(self, *args, **kargs):
        self.hist_filename = ".elapsed_time_hist"
    def start_run(self, examples, interpreters, filepath):
        self.filepath = filepath

        try:
            with open(self.hist_filename, 'r') as histfile:
                hist = json.load(histfile)[filepath]

            estimate_time = sum(hist) / len(hist)
        except:
            estimate_time = None

        self.begin = time.time()

    def end_run(self, failed, user_aborted, crashed):
        elapsed = time.time() - self.begin

        try:
            with open(self.hist_filename, 'r') as histfile:
                full_hist = json.load(histfile)
        except:
            full_hist = {}

        hist = full_hist.get(self.filepath, [])
        hist.append(elapsed)

        if len(hist) > 5:
            del hist[0]

        full_hist[self.filepath] = hist

        with open(self.hist_filename, 'w') as histfile:
            json.dump(full_hist, histfile)

