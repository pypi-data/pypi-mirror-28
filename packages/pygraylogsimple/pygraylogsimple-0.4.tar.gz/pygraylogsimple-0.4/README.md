# pygraylogsimple
Simple graylog lib that use offsets and limits to download all data (by default Graylog API limits messages to 150).
I used pycurl to fetch data and ThreadPool for multithreading.

## Installation

`pip install pygraylogsimple`

## Usage

Initialize class with username, password, host, limit for each request to API and logger function that accepts string as argument (optional)

`api = pygraylogsimple.PyGraylogSimple('user', 'pass', 'http://<host>:<port>', 100, <logger_func>)`

Call function with query and date_time from and to

`data = api.search_universal_absolute('*', '2017-07-01T00:00:00.000Z', '2017-07-02T00:00:00.000Z')`
