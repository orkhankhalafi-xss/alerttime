# AlertTime XSS Scanner

🛡️ **Advanced Multi-threaded XSS Vulnerability Scanner** with intelligent evasion capabilities and professional reporting.

**Author:** [Orkhan Khalafi](https://www.linkedin.com/in/orkhankhalafi/)  
**Version:** 2.5  
**License:** MIT

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-Testing-red.svg)](SECURITY.md)

## 🚀 Features

### Core Capabilities
- **🔥 High-Performance Multi-threading** - Up to 100 concurrent threads
- **🎯 Advanced Payload Arsenal** - 85+ sophisticated XSS vectors
- **🛡️ WAF Detection & Bypass** - Intelligent evasion for major providers
- **📊 Professional Reporting** - JSON, HTML, TXT, CSV formats
- **🥷 Stealth Scanning** - User-Agent rotation and request randomization
- **📝 POST Data Support** - Complete form testing capabilities

### Advanced Features
- **Polyglot XSS Vectors** - Multi-context injection payloads
- **Context-Aware Detection** - Smart payload generation
- **Real-time Progress Tracking** - ETA calculations and statistics
- **WAF Bypass Techniques** - Cloudflare, AWS, Akamai, Incapsula
- **Response Analysis** - Hash generation and duplicate detection
- **Professional HTML Reports** - Executive-level documentation

## 📦 Installation

### Quick Install
```bash
git clone https://github.com/orkhankhalafi/alerttime.git
cd alerttime
pip install -r requirements.txt
```

### Requirements
- Python 3.7+
- requests >= 2.28.0
- urllib3 >= 1.26.0
- colorama >= 0.4.4


### Basic Usage
```bash
# Simple scan
python3 alerttime.py -l targets.txt

# High-speed scan with HTML report
python3 alerttime.py -l targets.txt -t 40 --html-report

# POST data testing
python3 alerttime.py -l targets.txt --method POST --data "search=FUZZ&type=query"

# Stealth scan
python3 alerttime.py -l targets.txt -t 10 --delay 1.0
```

## 📖 Usage Examples

### Performance Scanning
```bash
# Maximum performance
python3 alerttime.py -l targets.txt -t 50 --delay 0.05

# Balanced performance
python3 alerttime.py -l targets.txt -t 25 --delay 0.15

# Conservative scanning
python3 alerttime.py -l targets.txt -t 10 --delay 0.5
```

### Output Formats
```bash
# JSON output (default)
python3 alerttime.py -l targets.txt -o results.json

# HTML professional report
python3 alerttime.py -l targets.txt --html-report

# CSV for analysis
python3 alerttime.py -l targets.txt --format csv -o report.csv

# Text format
python3 alerttime.py -l targets.txt --format txt -o report.txt
```

### Advanced Testing
```bash
# POST form testing
python3 alerttime.py -l targets.txt --method POST --data "username=FUZZ&password=test"

# Custom timeout and threads
python3 alerttime.py -l targets.txt -t 30 --timeout 15 --delay 0.1

# Verbose output
python3 alerttime.py -l targets.txt -v --html-report
```

## 🔧 Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `-l, --list` | Target URL list file (required) | - |
| `-o, --output` | Output file path | alerttime_scan.json |
| `--format` | Output format (json, txt, csv) | json |
| `--html-report` | Generate HTML report | False |
| `-t, --threads` | Concurrent threads (max: 100) | 25 |
| `--timeout` | Request timeout seconds | 10 |
| `--delay` | Inter-request delay seconds | 0.15 |
| `--method` | HTTP method (GET, POST) | GET |
| `--data` | POST data with FUZZ placeholder | - |
| `--user-agent` | Custom User-Agent string | - |
| `--verbose, -v` | Verbose output mode | False |

## 🛡️ Security Features

### WAF Detection & Bypass
- **Cloudflare** - Template literals, encoding variations
- **AWS WAF** - Case variations, character encoding  
- **Akamai** - Fragmentation, base64 encoding
- **Incapsula** - Unicode normalization
- **Generic WAFs** - Multiple encoding methods

### Stealth Capabilities
- **User-Agent Rotation** - 10+ realistic browser agents
- **Request Randomization** - Timing and header obfuscation
- **Connection Pooling** - Optimized for performance
- **SSL Bypass** - For authorized testing environments

### Payload Categories
- **Basic XSS** - Standard script injections
- **Event Handlers** - onload, onerror, onclick vectors
- **Encoded Payloads** - URL, Base64, HTML entity encoded
- **Context Breaking** - Quote and tag escape sequences
- **Polyglot Payloads** - Multi-context injection vectors
- **Modern Vectors** - HTML5 and ES6+ techniques

## 📊 Professional Reporting

### JSON Output
```json
{
  "scan_metadata": {
    "timestamp": "2026-12-19T10:30:00",
    "scanner": "AlertTime ",
    "version": "1.0",
    "author": "Orkhan Khalafi",
    "linkedin": "https://www.linkedin.com/in/orkhankhalafi/",
    "total_vulnerabilities": 5,
    "scan_duration": 120.5,
    "tests_performed": 2500,
    "success_rate": 0.2
  },
  "vulnerabilities": [...],
  "statistics": {...}
}
```

### HTML Reports
Professional HTML reports include:
- Executive dashboard with statistics
- Detailed vulnerability listings
- Severity classifications and risk assessment
- Author information and contact details
- Legal disclaimers and compliance notes

## ⚡ Performance Metrics

| Metric | Value |
|--------|-------|
| **Max Threads** | 100 concurrent |
| **Speed** | 100+ requests/second |
| **Payloads** | 85+ XSS vectors |
| **Formats** | 4 output formats |
| **WAF Support** | 10+ major providers |
| **Encoding** | 7+ methods |

## 🔒 Legal & Ethical Usage

### ⚠️ Important Disclaimer
This tool is for **authorized security testing only**. Unauthorized use is strictly prohibited. The author assumes no liability for illegal usage or damages caused by misuse of this software.

### Best Practices
- ✅ Obtain written authorization before testing
- ✅ Respect rate limits and server resources
- ✅ Follow responsible disclosure practices
- ✅ Comply with applicable laws and regulations
- ✅ Document all testing activities

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
git clone https://github.com/orkhankhalafi/alerttime.git
cd alerttime
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## 🔐 Security

For security issues, please see [SECURITY.md](SECURITY.md) for reporting guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Orkhan Khalafi**  
🔗 LinkedIn: https://www.linkedin.com/in/orkhankhalafi/  
📧 Professional security researcher and developer

---

## 🌟 Support

If you find this tool useful, please:
- ⭐ Star the repository
- 🐛 Report issues
- 💡 Suggest improvements
- 🤝 Contribute code

---

**AlertTime  v1.0** - Professional Security Testing Tool  

*Built with ❤️ for the security community*
