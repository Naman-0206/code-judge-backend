exit_codes = {
    0: "Successful exit without errors",
    1: "Runtime Error",
    2: "Incorrect usage, such as invalid options or missing arguments",
    124: "Time Limit Exceeded",
    125: "Compilation Error",
    127: "Command not found",
    137: "Memory Limit Exceeded",
    139: "Segmentation Fault",
    143: "Terminated by Signal",
    
    # Custom Exit Codes
    200: "Accepted",
    201: "Presentation Error",
    400: "Wrong Answer",
    401: "Error",  # File not found or Unknown Error
    402: "Message Parsing Error. See the logs for more details.",
    403: "Testing",
}
