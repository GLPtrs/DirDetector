# ⚡ DirDetector

**DirDetector** is a multithreaded Python tool for discovering hidden directories and files on web servers by brute-forcing URLs from a customizable wordlist. Supports filtering by HTTP status codes, file extensions, request delays, and proxy usage. Provides colored console output for easy identification of valid paths during penetration testing and web security assessments.

## 🔍 Features

- **Multithreaded scanning** with adjustable thread count__
- **File extension support** (e.g., `.php`, `.html`, etc.)    
- **Custom wordlists** to match specific targets  
- **Status code filtering** to only show desired responses (e.g., 200, 301, 403)  
- **Proxy support** for routing through tools like Burp Suite or ZAP  
- **Colored output** for fast visual feedback (via `colorama`)  
- **Optional delay** between requests to avoid detection or rate limits

## ⚙️ Installation and quick start

1. **Clone the repository**  
   ```bash
   git clone https://github.com/GLPtrs/DirDetector
   cd DirDetector

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Make the script executable (or use /usr/bin/env python3 DirDetector.py)**:
   ```bash
   chmod +x DirDetector.py
   ```

**Usage**:
   ```bash
   ./DirDetector.py <target> -w <wordlist> -x <extensions> (use -help for more options)
   ```
