# logdissect API
For program documentation, see [README.md](README.md)

The logdissect module contains utilities for parsing, storing, filtering, and exporting log data.

## Index
- [Introduction](#introduction)
- [Objects and Methods](#objects-and-methods)
  - [Parsers](#parsers)
  - [Data Objects](#data-objects)
- [Copyright](#copyright)

# Introduction
## Synopsis
    import logdissect
    myparser = logdissect.parsers.syslogbsd.ParseModule()
    attribute_dict = myparser.parse_line(<RAW_LINE>)
    logdataobject = myparser.parse_file(<LOG_FILE_PATH>)
    logentryobject = logdissect.data.LogEntry()

## Description
The logdissect module comes with the logdissect log analysis program. It contains objects which can be used to parse log lines and files, and store log information.

# Objects and Methods

## Parsers
### logdissect.parsers.\<parser>.ParseModule()
Replace \<parser\> with one of the available parsers:

- `` syslogbsd `` - standard syslog
- `` syslogiso `` - syslog with ISO 8601 datestamp
- `` nohost `` - syslog with no host attribute
- `` tcpdump `` - tcpdump terminal output
- `` ldjson `` - logdissect JSON output
    
Parsers have two methods (except the ldjson parser, which has no parse\_line() method):

#### parse\_file(\<file>)
Accepts a filename as input, and returns a LogData object (described below).

Parsers have a `tzone` attribute that uses standard ISO 8601 offset to UTC (e.g. `+0500`, `-0200`); if not set, logdissect will attempt to get current time zone data from the local system (unless a time zone is already present, such as in the syslogiso parser, or the ldjson parser).

#### parse\_line(\<line>)
Accepts a log line as input, and returns a dictionary of strings containing the following keys:

- `year` - a 4-digit string
- `month` - a 2-digit string
- `day` - a 2-digit string
- `tstamp` - a 6-digit string with optional decimal and extra places
- `tzone` - `+` or `-` followed by a 4-digit offset to utc (HHMM)
- `raw_stamp` - the raw stamp with attributes, as it was parsed
- `facility` - the log facility
- `severity` - the severity
- `source_host` - the source host
- `source_port` - the source port
- `source_process` - the source process
- `source_pid` - the source PID
- `dest_host` - the destination host
- `dest_port` - the destination port
- `protocol` - the protocol
- `message` - the message

Attributes that were not parsed will be returned as `None`. The ldjson parser has no parse\_line() method.

## Data Objects
### logdissect.data.LogEntry()
LogEntry is the data type for a single log entry. LogEntry objects have the following attributes:
- `parser`
- `date_stamp`
- `date_stamp_utc`
- `year`
- `month`
- `day`
- `tstamp`
- `tzone` - time zone
- `raw_text`
- `raw_stamp`
- `facility`
- `severity`
- `message`
- `source_path` - the file it was parsed from
- `source_host`
- `source_port`
- `source_process`
- `source_pid`
- `dest_host`
- `dest_port`
- `protocol`

LogEntry objects have one method:
- `_utc_date` - uses the datestamp and tzone to extrapolate a UTC timestamp

### logdissect.data.LogData()
LogData is the data type for a single log. LogData objects have the following attributes:
- `entries` - a list containing LogEntry objects
- `source_path` - the file it was parsed from
- `source_file`
- `source_file_mtime`
- `parser`

LogData objects have a few sorting methods:
- `` sort_time() `` - sorts entries by their `date_stamp_utc` attribute
- `` sort_path()  `` - sorts by path
- `` sort_facility `` - sorts by facility, then severity

### logdissect.data.LogDataSet()
LogDataSet is the data type for a logdissect project. LogDataSet objects have the following attributes:
- `data_set` - a list containing LogData objects
- `finalized_data` - a LogData object to hold all of the combined entries

LogDataSet objects have one method:
- `` merge_logs() `` - merges the logs in `data_set` into `finalized_data`, and sorts them using LogData's `sort_time()` method

# Copyright
MIT License

Copyright (c) 2017 Dan Persons (dpersonsdev@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
