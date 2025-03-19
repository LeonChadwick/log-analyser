# log-analyser
Assignment to analyse a log file and alert on conditions

This application parses its input data collecting statistics on time taken for jobs
that have logged their run start and end times and reporting those jobs
that exceed 5 minutes (as a warning) or exceed 10 minutes (as an error).

Log input is expected in CSV format.

Log columns are:
- HH:MM:SS timestamp
- Job description
- enum of {START|END}
- process id (PID)


# Open Questions To Enquire On With Stakeholder(s):
- is the whitespace on the START/STOP status column data guaranteed to be there or should whitespace stripping be implemented?
- would a job with same description running concurrently but with different pid be a valid scenario or should flag as error if detected?


Libraries required just during testing:
> pip install -r test-requirements.txt
 
