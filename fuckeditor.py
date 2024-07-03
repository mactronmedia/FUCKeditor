import random
import argparse
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from colorama import Fore, Style
from urllib3.exceptions import ConnectTimeoutError

R = '\033[91m'
B = '\033[94m'

banner = R + r"""
 __                _              _  _  _               
/ _|              | |            | |(_)| |              
| |_  _   _   ___ | | __ ___   __| | _ | |_  ___   _ __ 
|  _|| | | | / __|| |/ // _ \ / _` || || __|/ _ \ | '__|
| |  | |_| || (__ |   <|  __/| (_| || || |_| (_) || |   
|_|   \__,_| \___||_|\_\\___| \__,_||_| \__|\___/ |_|   
"""
coded_by = f"{B}FCKeditor Vulnerability Scanner by Mactron"

reset_color = '\033[0m'

print(f"{banner}{B}\n{coded_by}{reset_color}\n")

def get_formatted_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def write_to_file(message, filename):
    """Writes the message to the specified file."""
    with open(filename, 'a') as file:
        file.write(message + '\n')

def update_targets_file(targets, filename):
    """Writes the updated targets list back to the targets file."""
    with open(filename, 'w') as target_file:
        target_file.write('\n'.join(targets))

def main():
    parser = argparse.ArgumentParser(description='FCKeditor Vulnerability Scanner')
    parser.add_argument('-t', metavar='TARGETS_FILE', type=str, default='targets.txt',
                        help='Specify the targets file (default: targets.txt)')
    parser.add_argument('-f', '--full-scan', action='store_true', help='Perform a full scan using full_prefixes.txt')
    parser.add_argument('-q', '--quick-scan', action='store_true', help='Perform a common scan using common_prefixes.txt')
    args = parser.parse_args()

    if args.full_scan:
        prefixes_file = 'data/full_prefix.txt'
    elif args.quick_scan:
        prefixes_file = 'data/common_prefix.txt'
    else:
        prefixes_file = 'data/common_prefix.txt'

    with open(args.t, 'r') as target_file:
        targets = target_file.read().splitlines()

    with open(prefixes_file, 'r') as prefix_file:
        prefixes = prefix_file.read().splitlines()

    user_agent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

    while targets:
        selected_target = random.choice(targets)
        targets.remove(selected_target)

        for prefix in prefixes:
            if '://' in selected_target:
                url = f"{selected_target}/{prefix}"
            else:
                url = f"http://{selected_target}/{prefix}"

            timestamp = get_formatted_timestamp()

            try:
                response = requests.get(url, timeout=5, headers={'User-Agent': user_agent})
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.title.string.strip() if soup.title and soup.title.string else "No Title Found"

                    expected_titles = ["Resources Browser", "Server Browser", "FCKeditor - Resources Browser"]
                    if title in expected_titles:
                        success_message = f"{timestamp} - The title is '{title}' for {url}. URL has been written to 'success.txt'"
                        write_to_file(success_message, 'success.txt')
                        print(f"{timestamp} - {Fore.GREEN}{success_message}{Style.RESET_ALL}")
                    else:
                        print(f"{timestamp} - {Fore.YELLOW}The title is '{title}' for {url} and not one of the expected titles{Style.RESET_ALL}")
                else:
                    print(f"{timestamp} - {Fore.RED}Failed to retrieve the page for {url}. Status code: {response.status_code}{Style.RESET_ALL}")
            except ConnectTimeoutError:
                print(f"{timestamp} - {Fore.YELLOW}Skipped URL {url} due to a connection timeout error{Style.RESET_ALL}")
            except requests.exceptions.RequestException as e:
                print(f"{timestamp} - {Fore.RED}Error while connecting to {url}: {e}{Style.RESET_ALL}")

        update_targets_file(targets, args.t)

if __name__ == "__main__":
    main()