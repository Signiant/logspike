# logspike
Process NXLog messages and obfuscate sensitive information.

### Details

Logspike is designed to do the minimal amount of processing over a stream of log messages. It initiates with a series of regex patterns defined in patterns.py, compiles them and accepts a stream of log message data of a local TCP socket. Data comes in and logspike parses it into separate lines by using the newline character as the delimiter. It then goes through each regex until it finds the appropriate filter and performs obfuscation on the specified position(s) using regex groups. It then sends the data back out on a separate socket. 

As the data comes in as a fixed size, some messages may come in incomplete (i.e. no newline). When logspike runs into this condition, it will prepend the message to the buffer and append the next batch of data in order to get the complete message.
