import re
from collections import Counter

# Function to parse a single log line
def parse_log_line(line):
    # Regex pattern to parse Apache/Nginx combined log format
    pattern = re.compile(
        r'(?P<ip>\S+) '                      # IP address
        r'\S+ '                               # Ident (ignored)
        r'\S+ '                               # Auth (ignored)
        r'\[(?P<datetime>[^\]]+)\] '          # Date and time
        r'"(?P<request>[^"]+)" '              # Request (method, path, HTTP version)
        r'(?P<status>\d{3}) '                 # Status code
        r'(?P<size>\S+) '                     # Size of the response (could be '-')
        r'"(?P<referer>[^"]*)" '              # Referer
        r'"(?P<user_agent>[^"]*)"'            # User agent
    )
    
    match = pattern.match(line)
    if match:
        return match.groupdict()
    return None

# Function to analyze the log file
def analyze_log_file(log_file_path):
    with open(log_file_path, 'r') as file:
        lines = file.readlines()
    
    request_counter = Counter()
    status_counter = Counter()
    ip_counter = Counter()
    page_counter = Counter()
    
    for line in lines:
        log_data = parse_log_line(line)
        if log_data:
            request = log_data['request']
            status = log_data['status']
            ip = log_data['ip']
            
            request_counter[request] += 1
            status_counter[status] += 1
            ip_counter[ip] += 1
            
            # Extracting page from the request
            try:
                page = request.split(' ')[1]  # Splitting "GET /page HTTP/1.1" to get the page
                page_counter[page] += 1
            except IndexError:
                continue
    
    return request_counter, status_counter, ip_counter, page_counter

# Function to generate the report
def generate_report(log_file_path):
    request_counter, status_counter, ip_counter, page_counter = analyze_log_file(log_file_path)
    
    print("===== Web Server Log Analysis Report =====")
    
    # Number of 404 errors
    num_404_errors = status_counter.get('404', 0)
    print(f"Number of 404 errors: {num_404_errors}")
    
    # Most requested pages
    print("\nTop 10 Most Requested Pages:")
    for page, count in page_counter.most_common(10):
        print(f"{page}: {count} requests")
    
    # IP addresses with the most requests
    print("\nTop 10 IP Addresses with Most Requests:")
    for ip, count in ip_counter.most_common(10):
        print(f"{ip}: {count} requests")
    
    print("==========================================")

# Example usage
# Replace '/var/log/nginx/access.log' or '/var/log/apache2/access.log' with the actual path of web server's log file
log_file_path = '/var/log/nginx/access.log'  # For Nginx logs
# log_file_path = '/var/log/apache2/access.log'  # For Apache logs
generate_report(log_file_path)
