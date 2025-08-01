# 🔓 Optimized Password Cracker

A powerful password cracking tool with multilingual support, advanced optimizations, and colorful interface.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🌟 Features

### 🌍 Multilingual Support
- **Italiano (IT)** - Complete Italian interface
- **English (EN)** - Complete English interface
- Language selection at startup

### 🚀 Cracking Algorithms
- **Dictionary Attack**: Dictionary-based attack with case variations
- **Numeric Suffix Attack**: Adds numeric suffixes to dictionary words
- **Brute Force Attack**: Optimized parallel brute force attack
- **Case Variations**: Automatically generates uppercase/lowercase variations

### ⚡ Performance Optimizations
- **Memory Mapping**: Efficient loading of large files
- **Multiprocessing**: Parallel utilization of all CPU cores
- **Chunked Loading**: Block loading to handle huge dictionaries
- **Progress Tracking**: Real-time progress monitoring

### 🎨 User Interface
- **Colorama Integration**: Colored output for better readability
- **Real-time Progress**: Real-time progress indicators
- **Error Handling**: Robust error management
- **Cross-platform**: Compatible with Windows, Linux, macOS

## 📋 Requirements

### Python Dependencies
```
colorama
```

### Python Version
- Python 3.6 or higher

### Optional Files
- `common_passwords.txt` - Dictionary file (can be customized)

## 🚀 Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd password-cracker
```

### 2. Install dependencies
```bash
pip install colorama
```

### 3. Prepare dictionary file
Download or create a `common_passwords.txt` file with one password per line:
```
password
123456
admin
qwerty
letmein
```

## 📁 Project Structure

```
password-cracker/
├── main.py                    # Main script
├── common_passwords.txt       # Dictionary file
├── README.md                  # Documentation
└── requirements.txt           # Python dependencies
```

## 🎯 Usage

### Starting the Program
```bash
python main.py
```

### 1. Language Selection
```
Lingua/Language
1. IT (Italiano)
2. EN (English)

Choice: 2
```

### 2. Password Input
```
Enter password to crack: mypassword123
```

### 3. Dictionary Selection
```
Dictionary file (default: common_passwords.txt): 
```
Press enter to use the default file or specify a custom path.

### 4. Cracking Process
The program will automatically execute:
1. **Dictionary Attack** - Search for exact matches
2. **Suffix Attack** - Add numbers to dictionary words
3. **Brute Force** - Only for passwords ≤ 8 characters

## ⚙️ Advanced Configuration

### Dictionary Customization
- Supports files of any size
- One password per line
- UTF-8 encoding supported
- Automatic case variation handling

### Brute Force Optimizations
- **Length ≤ 4**: Keyspace `0-9a-z` (36 characters)
- **Length ≤ 6**: Keyspace `0-9a-zA-Z` (62 characters)  
- **Length > 6**: Keyspace `0-9a-zA-Z!@#` (65+ characters)

### Performance Limits
- **Dictionary Attack**: Unlimited (limited only by RAM)
- **Brute Force**: Recommended for passwords ≤ 8 characters
- **CPU Usage**: Uses all available cores (max 12 processes)

## 📊 Output Examples

### Successful Dictionary Attack
```
✓ Password found: 'Password123' in 45,672 attempts
```

### Successful Brute Force
```
Brute force: 8 processes, keyspace 36^4 = 1,679,616
✓ Password found: 'test' in 892,341 attempts
```

### Password Not Found
```
✗ Password not found in keyspace.
Total attempts: 1,679,616
```

## 🔧 Troubleshooting

### Dictionary File Not Found
```
Dictionary file common_passwords.txt not found
```
**Solution**: Create the file or specify a valid path.

### Memory Error
```
Error loading dictionary: MemoryError
```
**Solutions**: 
- Reduce dictionary size
- Increase system virtual memory
- Use a smaller dictionary file

### Slow Process
**Solutions**:
- Check that the dictionary isn't too large
- Monitor CPU usage in task manager
- For long passwords (>8 characters), use dictionary attack only

## ⚠️ Legal Warnings

### 🚨 RESPONSIBLE USE

**IMPORTANT**: This tool is intended exclusively for:
- Security testing on owned systems
- Recovering your own forgotten passwords
- Educational and research purposes
- Authorized security audits

### ❌ PROHIBITED USES
- Unauthorized access to others' systems
- Privacy violations
- Illegal activities of any kind
- Unauthorized commercial use

### 📜 Responsibility
The user is fully responsible for the use of this software. The developers assume no responsibility for misuse.

## 🤝 Contributing

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Improvement
- Adding new languages
- Algorithm optimizations
- User interface improvements
- Support for new dictionary formats
- Integration with external databases

## 📝 Changelog

### v2.0.0 (Current)
- ✅ Multilingual support (IT/EN)
- ✅ Colorized interface with Colorama
- ✅ Memory mapping optimizations
- ✅ Improved parallel brute force
- ✅ Robust error handling

### v1.0.0
- ✅ Basic dictionary attack
- ✅ Simple brute force
- ✅ Case variation support

## 🛡️ Security Considerations

### Ethical Use Guidelines
- Always obtain proper authorization before testing
- Use only on systems you own or have explicit permission to test
- Follow responsible disclosure practices
- Respect privacy and confidentiality

### Performance Impact
- Dictionary attacks are generally safe for system resources
- Brute force attacks can be CPU-intensive
- Monitor system temperature during extended use
- Consider impact on shared systems

## 📊 Performance Benchmarks

### Typical Performance (Intel i7-8700K)
- **Dictionary Attack**: ~500,000 attempts/second
- **Brute Force (4 chars)**: ~200,000 attempts/second
- **Memory Usage**: 50-500MB depending on dictionary size
- **CPU Usage**: 90-100% during brute force

### Optimization Tips
- Use SSD storage for better I/O performance
- Ensure adequate RAM for large dictionaries
- Close unnecessary programs during intensive cracking
- Use the most specific dictionary possible

## 🔍 Algorithm Details

### Dictionary Attack Flow
1. Load dictionary with memory mapping
2. Generate case variations for each word
3. Check direct password matches
4. Try numeric suffixes (1-4 digits)
5. Report results

### Brute Force Strategy
1. Determine optimal keyspace based on password length
2. Distribute work across available CPU cores
3. Generate combinations systematically
4. Check against password variations
5. Stop immediately when found

## 📞 Support

For bugs, questions, or suggestions:
- Open an Issue on GitHub
- Contact the development team
- Check existing documentation
- Review troubleshooting section

## 📄 License

This project is released under the MIT License. See the `LICENSE` file for details.

---

**⚡ Made with ❤️ for the cybersecurity community**
