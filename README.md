# Resource Usage Web Page  
A simple web page to monitor your system's resource usage.  


---

## Features 🌟  
- **Dynamic Background**: Changes color on each page refresh (cycles between 3 predefined colors).  
- **Host & Time Details**: Shows the hostname and current local datetime (updates on refresh).  
- **Resource Monitoring**:  
  - Application CPU/RAM usage.  
  - System-wide CPU/RAM usage.  
- **Always Visible**: A "Hello World!" header stays fixed at the top.  

---

## Installation and Usage

Follow these simple steps to get started:

### Clone the Repository and Navigate to the Directory
Open your terminal and run the following command:

```bash
git clone https://github.com/hambn/resource-usage-web-page.git ./resource-usage-web-page && cd ./resource-usage-web-page
```

### Run the Scripts
You can run either the Python or the Bash script, depending on your preference.

**To run the Python script:**
```bash
python3 script.py
```
**To run the Bash script:**
```bash
./script.sh
```
If you encounter a permission error, make sure to give the script execution permission:
```bash
chmod +x script.sh
```
### Viewing the Application
Once the script is running, the application should be visible in your browser at:
```
http://<your-ip>:5000
```
### Notes
- **Platform Compatibility:** Both scripts are designed to work on Unix-like systems. Ensure you have the required interpreters installed (Python 3 for `script.py` and Bash for `script.sh`).
- **Dependencies:** No additional packages are required; both scripts utilize built-in commands and modules.

---

## Why Use This? 🛠️  
- Quickly check your system’s performance through a web browser.  
- No complex setup—just run the app and open the page.  
- Lightweight and easy to customize.  

---

## How It Works 🔄  
1. **Refresh the Page**:  
   - Background color changes.  
   - Datetime, application, and system resource stats update.  
2. **Stats Displayed**:  
   - **Host**: Name of the machine running the app.  
   - **Local Datetime**: Current time on the host.  
   - **Application Usage**: CPU and RAM consumed by the app itself.  
   - **System Usage**: Total CPU and RAM used by the entire system.  

---

## Notes 📝
- Stats update only when you refresh the page (not real-time).
- Its dockerized and works on Linux, Windows, and macOS.
- Customize colors by editing the `background_colors` list in the code.


