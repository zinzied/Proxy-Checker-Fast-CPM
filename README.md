The provided code is a Python script that checks the availability of proxies and categorizes them as either working or dead. It uses a graphical user interface (GUI) built with Tkinter to allow users to input a list of proxies, specify an output file, set the number of threads, and define a timeout value for checking each proxy. The script supports both HTTP/HTTPS and SOCKS4/SOCKS5 proxies.

### Key Features:
1. **Proxy Checking**:
   - The script checks if a proxy is alive by attempting to connect to it and make a request to a specified URL (e.g., Google).
   - It distinguishes between SOCKS4, SOCKS5, and HTTP/HTTPS proxies.

2. **Multithreading**:
   - The script uses multiple threads to check proxies concurrently, improving the speed of the checking process.

3. **GUI**:
   - The Tkinter-based GUI allows users to:
     - Select a file containing a list of proxies.
     - Specify an output file to save working proxies.
     - Set the number of threads for concurrent checking.
     - Set a timeout value for each proxy check.
     - Start and stop the proxy checking process.
     - View progress and log messages in real-time.
     - See counters for dead and working proxies.

4. **Logging and Progress Tracking**:
   - The script logs messages with different colors to indicate errors, alerts, and actions.
   - It updates a progress bar and counters for dead and working proxies as the checking process progresses.

### Description:
This script is designed to help users verify the availability of a large number of proxies efficiently. By leveraging multithreading and a user-friendly GUI, it simplifies the process of identifying working proxies from a given list. The script is useful for anyone who needs to manage and validate proxy lists, such as network administrators, developers, and researchers.

### Example Usage:
1. **Load Proxy List**: Use the "Browse" button to select a file containing proxies in the format `host:port`, one per line.
2. **Specify Output File**: Use the "Browse" button to select or create a file where working proxies will be saved.
3. **Set Parameters**: Enter the number of threads and the timeout value in seconds.
4. **Start Checking**: Click the "Start" button to begin the proxy checking process.
5. **Monitor Progress**: Watch the progress bar, log messages, and counters to see the status of the checking process.
6. **Stop Checking**: Click the "Stop" button to halt the checking process if needed.

### Example GUI Layout:
- **Proxy list**: Entry field and "Browse" button to select the proxy list file.
- **Output file**: Entry field and "Browse" button to select the output file.
- **Number of threads**: Entry field to specify the number of threads.
- **Timeout (seconds)**: Entry field to specify the timeout value.
- **Start**: Button to start the proxy checking process.
- **Stop**: Button to stop the proxy checking process.
- **Progress Bar**: Displays the progress of the proxy checking process.
- **Log Text**: Text area to display log messages.
- **Counters**: Labels to display the number of dead and working proxies.

This script provides a comprehensive solution for proxy validation with a focus on usability and efficiency.

[<img src="https://github.com/zinzied/Website-login-checker/assets/10098794/24f9935f-3637-4607-8980-06124c2d0225">](https://www.buymeacoffee.com/Zied)
