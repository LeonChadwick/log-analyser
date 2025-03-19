""" unit tests for the log_analyser """
import logging
from unittest import mock

from log_analyser import LogAnalyser
from log_parser import parse_log

class TestLogAnalyser:

    analyser = LogAnalyser()
    logger = logging.getLogger("log_analyser")

    def _assert_log_counts(self, mock_log, warnings: int, errors: int):
        """ helper to accumulate counts of log calls and assert they match expected counts """
        assert len(mock_log.call_args_list) == warnings+errors
        found_warnings = 0
        found_errors = 0
        for c in mock_log.call_args_list:
            match c.args[0]:
                case logging.WARNING:
                    found_warnings += 1
                case logging.ERROR:
                    found_errors += 1

        assert warnings == found_warnings
        assert errors == found_errors


    def _capture_logging_for_data(self, data):
        """ helper to mock the logger, run the processing on the given data and return the mock for analysis """
        with mock.patch.object(self.logger, 'log') as mock_log:
            for ll in parse_log(data):
                self.analyser.process_line(ll)
        return mock_log

    def test_clean_case(self):
        """ log sample with no alertable cases """

        data = """\
    11:36:11,scheduled task 796, START,57672
    11:36:18,scheduled task 796, END,57672""".splitlines()

        mock_log = self._capture_logging_for_data(data)
        self._assert_log_counts(mock_log,0, 0)

    def test_warn_case(self):
        """ log sample that should trigger warn level logging """

        data = """\
    11:36:11,scheduled task 796, START,57672
    11:42:18,scheduled task 796, END,57672""".splitlines()

        mock_log = self._capture_logging_for_data(data)
        self._assert_log_counts(mock_log,1, 0)

    def test_error_case(self):
        """ log sample that should trigger warn level logging """

        data = """\
    11:36:11,scheduled task 796, START,57672
    11:46:18,scheduled task 796, END,57672""".splitlines()

        mock_log = self._capture_logging_for_data(data)
        self._assert_log_counts(mock_log,0, 1)


    def test_nostart_case(self):
        """ log sample with no alertable cases """

        data = """\
    11:36:18,scheduled task 796, END,57672""".splitlines()

        mock_log = self._capture_logging_for_data(data)
        self._assert_log_counts(mock_log,0, 0)

    def test_nostart_case(self):
        """ log sample with no alertable cases """

        data = """\
    11:36:18,scheduled task 796, END,57672""".splitlines()

        mock_log = self._capture_logging_for_data(data)
        self._assert_log_counts(mock_log,0, 0)

    def test_noend_case(self):
        """ log sample with no alertable cases """

        data = """\
    11:36:11,scheduled task 796, START,57672""".splitlines()

        mock_log = self._capture_logging_for_data(data)
        self._assert_log_counts(mock_log,0, 0)

