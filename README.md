### README Description

**Proxy Checker Application**

![image](https://github.com/user-attachments/assets/919936b0-74a6-4c64-968d-c58d436208a9)


This project is a Python-based application designed to check the availability of proxies and categorize them as either working or dead. It features a graphical user interface (GUI) built with CustomTkinter, allowing users to easily manage and monitor the proxy checking process.

**Key Features:**
- **Proxy Checking:** Supports both HTTP/HTTPS and SOCKS4/SOCKS5 proxies.
- **Multithreading:** Utilizes multithreading to enhance the speed and efficiency of the proxy checking process.
- **GUI Interface:** Provides an intuitive GUI for loading proxy lists, setting parameters, and monitoring progress.
- **Logging and Progress Tracking:** Displays log messages and progress updates in real-time.

**Getting Started:**
1. **Load a Proxy List:** Select a file containing proxies in the format `host:port`, one per line.
2. **Specify an Output File:** Choose where the working proxies will be saved.
3. **Set Parameters:** Define the number of threads and the timeout value for each proxy check.
4. **Start Checking:** Click the "Start" button to begin the proxy checking process.
5. **Monitor Progress:** Use the progress bar, log messages, and counters to track the process.
6. **Pause/Resume/Stop:** Pause, resume, or stop the checking process as needed.

**Example GUI Layout:**
- Proxy list input
- Output file input
- Number of threads
- Timeout setting
- Start, Stop, and Pause/Resume buttons
- Progress bar
- Log text area
- Counters for dead and working proxies

### Requirements

To run this application, you need to have the following Python packages installed. You can list these in a `requirements.txt` file:

**File: requirements.txt**
```
customtkinter
```

To install the required packages, you can use the following command:

```bash
pip install -r requirements.txt
```

This setup ensures that the application has all the necessary dependencies to function correctly.
