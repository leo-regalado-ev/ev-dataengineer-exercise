import time


class ExecutionTimeLogger():
    """
        Reusable execution time logger class
    """

    def __init__(self):
        self.reset_time()

    def reset_time(self):
        """
            Sets the start time to current time
        """
        self.start_time = time.time()

    def log_current_time(self, message="Current runtime"):
        """
            Logs the seconds since start_time\n
            Parameters:\n
            message - A message string before printing seconds,
                for labeling certain points in the code
        """
        current_seconds = time.time() - self.start_time
        print(f"{message}: {current_seconds} seconds ---")
