# Auto-PPPoE

An automated PPPoE credential management system that intelligently switches between multiple internet accounts based on usage limits.

## Overview

This project automatically manages PPPoE connections by:
- Monitoring usage limits for multiple internet accounts
- Automatically switching to available accounts when limits are reached
- Providing a tiered fallback system for uninterrupted connectivity

## System Compatibility

**Important Notes**: 
- This code is specifically designed for **IUT's PPPoE system** 
- Router compatibility is tested with the **Cudy-WR1300** router

## Router Compatibility 

If you are using a different router model or brand, you will need to modify the router login and PPPoE setup/status check functionalities in the following files:
- `PPPoE_checker.py` - Contains router status checking logic
- `PPPoE_setter.py` - Contains PPPoE credential setting logic

### Adapting for Other Routers

To adapt this code for your router:

1. **Use Burp Suite or similar tools** to intercept and analyze the HTTP requests your router uses for:
   - Login authentication
   - PPPoE configuration pages
   - Status checking endpoints
   
2. **Modify the following in the relevant files**:
   - Router URL endpoints
   - Login form parameters
   - CSRF token handling (if required)
   - PPPoE configuration form fields
   - Response parsing logic

3. **Key areas to analyze**:
   - Login POST request format and parameters
   - Session management (cookies, tokens)
   - PPPoE configuration form structure
   - Status response format (JSON/HTML parsing)

The current implementation uses Cudy router's specific web interface endpoints and form structures. Different router manufacturers use different web interfaces and form formats.

## Installation & Setup

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/ahsanbulbul/Auto-PPPoE.git
   cd Auto-PPPoE
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure database**
   
   Create `credentials.db` using the provided setup file:
   ```bash
   sqlite3 credentials.db < database_setup.sql
   ```
   
   **Reference**: See `database_setup.sql` for the complete structure and `test.db` for example format.

4. **Test the setup**
   ```bash
   python PPPoE_Automation.py
   ```

## 📋 Usage

### Manual Execution

**Linux/macOS:**
```bash
./runLinux.sh
```

**Windows:**
```batch
runWindows.bat
```

**Direct Python:**
```bash
python PPPoE_Automation.py
```

### Automated Execution

**Crontab**

For periodic automatic checking and switching:

```bash
crontab -e
```

Add the following line to check every hour at minute 42:
```bash
# Auto-PPPoE - Check and switch PPPoE credentials hourly
42 * * * * /opt/Auto-PPPoE/runLinux.sh
```