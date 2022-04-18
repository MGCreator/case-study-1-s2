import win32evtlog
import platform

uname = platform.uname()
server_name = uname.node

source_name =  ['System', 'Application', 'Security']
h = win32evtlog.OpenEventLog(server_name, "Application")

flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
records = win32evtlog.ReadEventLog(h, flags, 0)
print(len(records))
for record in records:
    print(record.SourceName)
    print(record.TimeWritten.Format())
