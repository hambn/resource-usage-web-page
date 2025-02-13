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


