import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def fetch_status(ip):
    """
    Fetch the HTTP status code for a given IP.

    :param ip: The IP address to check
    :return: A tuple of the IP and its status code or an error
    """
    url = f"http://{ip}"
    try:
        response = requests.get(url, timeout=2)
        return ip, response.status_code
    except requests.exceptions.RequestException:
        return ip, None

def display_result(ip, status_code):
    """
    Display the result with color-coded status codes.

    :param ip: The IP address
    :param status_code: The HTTP status code
    """
    if status_code == 200:
        color = Fore.GREEN
    elif status_code in [301, 303]:
        color = Fore.BLUE
    elif status_code == 403:
        color = Fore.RED
    elif status_code == 500:
        color = Fore.WHITE
    else:
        color = Fore.YELLOW

    if status_code:
        print(f"IP: {ip}, Status Code: {color}{status_code}{Style.RESET_ALL}")
    else:
        print(f"IP: {ip} is {Fore.RED}unresponsive or unreachable{Style.RESET_ALL}.")

def fetch_ip_status_parallel(file_path):
    """
    Reads IPs from a given file, checks their HTTP status codes in parallel,
    and displays color-coded results.

    :param file_path: Path to the file containing IP addresses (one per line)
    """
    try:
        with open(file_path, 'r') as file:
            ips = [line.strip() for line in file if line.strip()]

        if not ips:
            print("The file is empty or contains no valid IPs.")
            return

        print("\nChecking IPs for status codes:\n")

        with ThreadPoolExecutor() as executor:
            future_to_ip = {executor.submit(fetch_status, ip): ip for ip in ips}

            for future in as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    ip, status_code = future.result()
                    display_result(ip, status_code)
                except Exception as e:
                    print(f"Error checking IP {ip}: {e}")

    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example Usage
if __name__ == "__main__":
    file_path = input("Enter the path to the file containing IP addresses: ")
    fetch_ip_status_parallel(file_path)
