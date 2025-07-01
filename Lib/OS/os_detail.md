
# Why Use the os Module in DevOps?
1) Automation: Automate file operations, directory management, or system configuration tasks.
2) System Administration: Access system details, manage permissions, or execute commands.
3) Cross-Platform Compatibility: Write scripts that work across different operating systems.
4) Environment Management: Access and modify environment variables for configuration.
5) Process Control: Manage running processes or execute system commands.

# Key Functions and Methods in the os Module for DevOps
Below, I’ve categorized the most relevant os module functions for DevOps operations, explaining their purpose, usage, and real-world DevOps examples. I’ve focused on functions that align with tasks like cloud automation, system administration, monitoring, and process management.

1. File and Directory Operations
These functions are critical for managing filesystems, which is common in DevOps for tasks like log file handling, configuration management, and deployment automation.

---

# os.path.join(path, *paths)
- Purpose: Combines path components intelligently, using the correct path separator (/ for Unix, \ for Windows).
- DevOps Use Case: Create file paths for scripts that manage logs, configurations, or backups across platforms.

=> Example: 
`Create a cross-platform path for a log file`

```py
import os

log_dir = "logs"
log_file = "app.log"

full_path = os.path.join(log_dir, log_file)

print(f"Log file path: {full_path}")  # Output: logs/app.log (Unix) or logs\app.log (Windows)
```

---

# os.makedirs(path, exist_ok=True)
- Purpose: Creates directories recursively, like mkdir -p in Unix. If exist_ok=True, it won’t raise an error if the directory exists.
- DevOps Use Case: 
Set up directory structures for deployments, logs, or temporary files.

=> Example: 
`Create a directory for storing application backups`

```py
import os

backup_dir = "backups/2025/06"
os.makedirs(backup_dir, exist_ok=True)
print(f"Created directory: {backup_dir}")
```

---

# os.listdir(path)
- Purpose: Returns a list of entries in the specified directory.
- DevOps Use Case: Scan directories for log files, configuration files, or deployment artifacts.

=> Example: 
`List all log files in a directory`

```py
import os

log_dir = "logs"
files = os.listdir(log_dir)
log_files = [f for f in files if f.endswith(".log")]
print(f"Log files: {log_files}")
```

---

# os.remove(path) and os.unlink(path)
- Purpose: Deletes a file. Both functions are equivalent.
- DevOps Use Case: Clean up temporary files or old logs during maintenance tasks.

=> Example: 
`Delete old log files`

```py
import os

log_file = "logs/old.log"
if os.path.exists(log_file):
    os.remove(log_file)
    print(f"Deleted: {log_file}")
```

---

# os.rename(src, dst)
- Purpose: Renames or moves a file or directory.
- DevOps Use Case: Rename log files during rotation or move files during deployments.

=> Example: 
`Rename a log file with a timestamp.`

```py
import os
from datetime import datetime

old_name = "logs/app.log"
timestamp = datetime.now().strftime("%Y%m%d")
new_name = f"logs/app_{timestamp}.log"
if os.path.exists(old_name):
    os.rename(old_name, new_name)
    print(f"Renamed {old_name} to {new_name}")
```

---

# os.path.exists(path)
- Purpose: Checks if a file or directory exists.
- DevOps Use Case: Validate the presence of configuration files or directories before performing operations.

=> Example: 
`Check if a configuration file exists.`

```py
import os

config_file = "/etc/myapp/config.yaml"
if os.path.exists(config_file):
    print("Configuration file found!")
else:
    print("Configuration file missing!")
```

---

# os.walk(top)
- Purpose: Recursively traverses a directory tree, yielding tuples of (dirpath, dirnames, filenames).
- DevOps Use Case: Find all files in a directory structure, e.g., for backup or log analysis.

=> Example: 
`Find all .log files recursively`

```py
import os

for dirpath, dirnames, filenames in os.walk("logs"):
    for filename in filenames:
        if filename.endswith(".log"):
            print(os.path.join(dirpath, filename))
```

=======================================


2. Environment Variables
Environment variables are crucial in DevOps for configuration management and secure credential handling.

# os.environ
- Purpose: A dictionary-like object for accessing and modifying environment variables.
- DevOps Use Case: Access configuration settings or credentials without hardcoding them in scripts.

=> Example: 
`Get and set an environment variable for an AWS access key.`

```py

import os

# Get an environment variable
aws_key = os.environ.get("AWS_ACCESS_KEY_ID", "not-set")
print(f"AWS Key: {aws_key}")

# Set an environment variable
os.environ["APP_ENV"] = "production"
print(f"Set APP_ENV to: {os.environ['APP_ENV']}")
```

---

# os.getenv(key, default=None)
- Purpose: Retrieves an environment variable’s value, with an optional default if not found.
- DevOps Use Case: Safely access configuration settings.

=> Example: 
`Get a database URL with a fallback`

```py

import os

db_url = os.getenv("DATABASE_URL", "sqlite:///default.db")
print(f"Database URL: {db_url}")
```

=======================================


3. Process Management
These functions help manage processes, which is essential for automation and system administration in DevOps.

# os.system(command)
- Purpose: Executes a shell command and returns the exit status.
- DevOps Use Case: Run shell commands like restarting services or deploying applications.

=> Example: 
`Restart a web server`

```py

import os

exit_status = os.system("sudo systemctl restart nginx")
if exit_status == 0:
    print("Nginx restarted successfully")
else:
    print("Failed to restart Nginx")
```

---

# os.popen(command)
- Purpose: Executes a command and opens a pipe to read its output or send input.
- DevOps Use Case: Capture output from system commands (e.g., checking disk usage).

=> Example: 
`Check disk usage`

```py

import os

output = os.popen("df -h").read()
print("Disk Usage:\n", output)
```

---

# os.getpid()
- Purpose: Returns the current process ID.
- DevOps Use Case: Log the process ID for debugging or monitoring scripts.

=> Example: 
`Log the script’s PID`

```py

import os

pid = os.getpid()
print(f"Script running with PID: {pid}")
```

---

# os.kill(pid, signal)
- Purpose: Sends a signal to a process (Unix only).
- DevOps Use Case: Terminate or signal processes during system maintenance.

=> Example: 
`Terminate a process by PID`

```py

import os
import signal

pid = 12345  # Example PID
try:
    os.kill(pid, signal.SIGTERM)
    print(f"Sent SIGTERM to PID {pid}")
except OSError as e:
    print(f"Error: {e}")
```

=======================================


4. System Information
These functions provide system details, useful for monitoring and administration.

# os.uname() (Unix only)
- Purpose: Returns system information (e.g., OS name, hostname, kernel version).
- DevOps Use Case: Gather system details for inventory or monitoring.

=> Example: 
`Get system info`

```py

import os

try:
    info = os.uname()
    print(f"System: {info.sysname}, Host: {info.nodename}, Version: {info.release}")
except AttributeError:
    print("os.uname() not available on this platform")
```

---

# os.cpu_count()
- Purpose: Returns the number of CPU cores available.
- DevOps Use Case: Optimize resource usage in automation scripts.

=> Example: 
`Check CPU count for load balancing`

```py

import os

cores = os.cpu_count()
print(f"Number of CPU cores: {cores}")
```

=======================================


5. File Permissions and Ownership
These functions are useful for managing file access, especially in secure environments.

# os.chmod(path, mode)
- Purpose: Changes file permissions (Unix-style, e.g., 0o755).
- DevOps Use Case: Secure configuration files or scripts during deployment.

=> Example: 
`Set executable permissions for a script`

```py

import os

script = "deploy.sh"
os.chmod(script, 0o755)  # Owner: rwx, Group/Other: r-x
print(f"Set permissions for {script}")
```

---

# os.chown(path, uid, gid) (Unix only)
- Purpose: Changes file ownership.
- DevOps Use Case: Assign ownership to specific users or groups for security.

=> Example: 
`Change ownership of a configuration file`

```py

import os

config_file = "/etc/myapp/config.yaml"
try:
    os.chown(config_file, 1000, 1000)  # Example UID and GID
    print(f"Changed ownership of {config_file}")
except OSError as e:
    print(f"Error: {e}")
```

=======================================


6. Working Directory Management
These functions help manage the script’s working directory, useful in deployment and automation.

# os.getcwd()
- Purpose: Returns the current working directory.
- DevOps Use Case: Verify or log the directory context of a script.

=> Example: 
`Print the current directory`

```py

import os

current_dir = os.getcwd()
print(f"Current working directory: {current_dir}")
```

---

# os.chdir(path)
- Purpose: Changes the current working directory.
- DevOps Use Case: Switch directories for operations like deployments or backups.

=> Example: 
`Change to a deployment directory`

```py

import os

deploy_dir = "/var/www/html"
os.chdir(deploy_dir)
print(f"Changed to directory: {os.getcwd()}")
```

=======================================


7. Path Manipulation (via os.path)
These functions handle file paths, ensuring cross-platform compatibility.

# os.path.abspath(path)
- Purpose: Returns the absolute path of a file or directory.
- DevOps Use Case: Ensure consistent path references in scripts.

=> Example: 
`Get the absolute path of a file`

```py

import os

file_path = "logs/app.log"
abs_path = os.path.abspath(file_path)
print(f"Absolute path: {abs_path}")
```

---

# os.path.basename(path) and os.path.dirname(path)
- Purpose: Extract the file name or directory from a path.
- DevOps Use Case: Parse paths for log or configuration file processing.

=> Example: 
`Extract file and directory names`

```py

import os

path = "/var/log/app.log"
file_name = os.path.basename(path)  # app.log
dir_name = os.path.dirname(path)    # /var/log
print(f"File: {file_name}, Directory: {dir_name}")
```

---


``` Practical DevOps Scenarios Using the os Module ```
To make this actionable, here are some real-world DevOps scenarios where the os module shines, with complete code examples:

# Scenario 1: Log File Cleanup Script
Task: Delete log files older than 7 days to free up disk space.

```py
import os
import time
from datetime import datetime, timedelta

log_dir = "logs"
days_old = 7
threshold = time.time() - (days_old * 86400)  # Seconds in 7 days

for dirpath, _, filenames in os.walk(log_dir):
    for filename in filenames:
        if filename.endswith(".log"):
            file_path = os.path.join(dirpath, filename)
            if os.path.getmtime(file_path) < threshold:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
```
- Why Use os?: os.walk traverses directories, os.path.join builds paths, os.path.getmtime checks modification time, and os.remove deletes files.
- DevOps Context: Schedule this script with a cron job or CI/CD pipeline to automate log cleanup.

---

Scenario 2: Environment-Based Configuration
Task: Load configuration based on an environment variable.

```py
import os

env = os.environ.get("APP_ENV", "development")
config_file = os.path.join("config", f"{env}.yaml")

if os.path.exists(config_file):
    print(f"Loading configuration from: {config_file}")
else:
    print(f"Configuration file not found: {config_file}")
```

- Why Use os?: os.environ.get accesses environment variables, and os.path functions handle file paths.
- DevOps Context: Use in deployment scripts to load environment-specific configurations (e.g., dev, prod).

---

# Scenario 3: System Health Check
Task: Check disk space and log the results.

```py
import os

def check_disk_space(path="."):
    stat = os.statvfs(path)  # Unix only; use psutil for cross-platform
    free_space = stat.f_bavail * stat.f_frsize / (1024 ** 3)  # GB
    print(f"Free disk space at {path}: {free_space:.2f} GB")

check_disk_space("/")
```

- Why Use os?: os.statvfs provides filesystem statistics (Unix-only).
- DevOps Context: Use in monitoring scripts to alert on low disk space.

---

# Scenario 4: Deployment Directory Setup
Task: Create a deployment directory structure and set permissions.

```py
import os

deploy_dir = "deploy/app"
os.makedirs(deploy_dir, exist_ok=True)
os.chmod(deploy_dir, 0o755)  # Set permissions
print(f"Created and configured: {deploy_dir}")
```

- Why Use os?: os.makedirs creates directories, and os.chmod sets permissions.


=========================================================================