
An assignment for parsing and reporting based upon logged data.

# Project Files

- README.md - this document
- log_analyser.py - the application that implements the specified requirement in terms of reporting of alertable conditions via logging 
- log_parser.py - helper logic for the selection, consumption and interpretation of a log file in the prescribed format.
- logs.log - a sample of logs content
- test-requirements.txt - Python requirements file that lists libraries/versions required for a project (in this case just for testing, not for runtime)
- test_log_analyser.py - some unti tests of the base cases with helper logic to make addition of more test cases very simple with less boilerplate

# Running the application

The app will determine if a log file parameter has been given to it and if not, resort to reading input from stdin.
Examples of running the app on a Unix command line:

- python log_analyser.py <log-file>
- cat <log-file> | python log_analyser.py
- tail -F <log-file> | python log_analyser.py


# Running the tests

Install libraries required for the testing (may require an upgrade of pip to latest first):
- pip install -r test-requirements.txt

Running the tests:
- python -m pytest test_log_analyser.py

# Commentary on the assigned task

1. Fire and Forget vs Stakeholder Feedback Loop
2. Stakeholder Questions raised
3. Logs vs Metrics - Logs for alerting are of a bygone age
4. Additional directions to take if more investment warranted


### 1. Fire and Forget vs Stakeholder Feedback Loop

This assignment illustrates well that contact with stakeholders is important to prevent a project going in the wrong direction.
The assignment doesn't specify typical operating conditions in which it may be used, volumes of activity being processed etc.
As a result, in the absence of contact, some assumptions had to be made which may not align with expectations,
though I have documented the questions that could have arisen as I went along.


### 2. Stakeholder Questions raised

- is the whitespace on the START/STOP status column data guaranteed to be there? (i.e. should whitespace stripping be implemented). 
  recommend stripping the whitespace at source rather than in this app
- would a job with same description running concurrently but with different pid be a valid scenario or should we flag as error if detected?
- Our log file rollover may have missed out the start of a job but our log captured the end, we don't have sufficient information to track elapsed time
  could take a guess on START based upon the first timestamp in the file as being the earliest possible START, but what should we do precisely?
- there is a question of whether logs we operate with can roll over to the next day, if so the timestamps could
  go backwards breaking the elapsed time calculation, we might also have jobs that took >24 hours to run so it would look like the timestamps
  went forwards perhaps just for a short while when in fact a job took ages (i.e. a missed edge case). would recommend addition of date in ISO format to the logs


### 3. Logs vs Metrics - Logs for alerting are of a bygone age

Scraping logs for this kind of alerting is very old school (10+ years out of date in its approach), a migration to utilise metric based
reporting and alerting is the current recommended approach.  Having apps report metrics directly to a metric or timeseries database such
as Prometheus or InfluxDB could mean this app could be deleted and the metrics used directly in an alerting tool.
Alerting tools make changing the alert conditions much easier and in a centralised place, instead of having to change and re-release this app
if say the 5 and 10 minute alert conditions needed to be changed, which is more painful.
Additionally, metrics are queryable and could be used for many other purposes beyond alerting, such as run duration analysis, workload/host distribution, job/cpu usage etc.


### 4. Additional directions to take if more investment warranted

- Implement usage of argparse library as all Python command line apps should standardise on that to make app maintenance consistent for developers 
- Implement throttling by default into the code so that it can't eat all cpu on production machine unless asked to override that setting.
- Migrate to pandas if a more batch oriented approach is warranted as that removes some need for the parsing logic to be maintained,
  but at the expense that running directly on a production machine could have impact upon the production performance.
- Add test for edge case where job has multiple ends for a single start
- Add test for edge case where timestamp rolls over into next day.
- Add test case for job with same description running concurrently but with different pid
- Implement metrics in the app to report counts of activity processed and alertable scenarios detected, if the app is run in a continuous
  mode then such metrics could be used to detect and alert that this log analyser itself has become stuck if the activity count doesn't progress.

# Application Description

This application parses its input data collecting statistics on time taken for jobs
that have logged their run start and end times and reporting those jobs
that exceed 5 minutes (as a warning) or exceed 10 minutes (as an error).

A suggested mode of operation is to run with this command line:
tail -F logs.log | python log_analyser.py

This will handle log rotations that maybe happening on the underlying file and allow the analyser
to maintain its state when the log roles so that stops/starts across multiple log files are better tracked.

Log input is expected in CSV format and is headerless, i.e. the first row is data just like all the other rows.

Log columns are:
- HH:MM:SS timestamp
- Job description
- enum of {START|END}
- process id (PID)


