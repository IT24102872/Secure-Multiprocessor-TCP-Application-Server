# Secure Multiprocessor TCP Application Server

A robust, production-grade TCP application server implemented in C with secure authentication, session management, and concurrent client handling using multiprocessing. This project demonstrates network programming, cryptography, and system programming concepts for the IE2102 Network Programming module.

**Module:** IE2102 - Network Programming  
**Student ID:** IT24102872  
**Port:** 50872  
**Language:** C (Server) + Python (Client)

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Building](#installation--building)
- [How to Run](#how-to-run)
- [Usage Guide](#usage-guide)
- [Architecture & Design](#architecture--design)
- [Security Features](#security-features)
- [Protocol Specification](#protocol-specification)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

This project implements a **Secure Multiprocessor TCP Application Server** that:

- Handles **multiple concurrent clients** using fork-based multiprocessing
- Provides **secure user authentication** with PBKDF2-HMAC-SHA256 password hashing
- Manages **session tokens** with automatic timeout and expiration
- Implements **rate limiting** and **lockout protection** against brute-force attacks
- Uses **LEN-framed message protocol** for reliable communication
- Logs all operations to a centralized log file
- Supports user registration, authentication, and session-based operations

---

## ✨ Key Features

### Security
- ✅ **PBKDF2-HMAC-SHA256** password hashing with 100,000 iterations
- ✅ **Cryptographically secure tokens** generated with OpenSSL RAND_bytes
- ✅ **Rate limiting** (max 10 requests/second per client)
- ✅ **Automatic account lockout** (3 failed login attempts = 300s lockout)
- ✅ **Session expiration** (5-minute token timeout)
- ✅ **File locking** (flock) for concurrent database access

### Robustness
- ✅ **Multiprocessing architecture** - each client gets dedicated process
- ✅ **Multiple message buffering** - handles multiple frames in single recv()
- ✅ **Payload validation** - oversized/malformed frame protection
- ✅ **Signal handling** - proper SIGCHLD reaping with WNOHANG
- ✅ **Connection resilience** - socket reuse with SO_REUSEADDR

### Functionality
- ✅ User registration and login
- ✅ Session-based authentication
- ✅ Echo, status, and info commands
- ✅ Comprehensive logging with timestamps
- ✅ Dynamic directory creation

---

## 📁 Project Structure

```
Secure-Multiprocessor-TCP-Application-Server/
├── README.md                      # Project documentation (this file)
├── Makefile_2872                  # Build configuration
├── server_2872.c                  # Main server implementation (C)
├── server_2872                    # Compiled server binary
├── client_2872.py                 # Client application (Python)
├── test_concurrent.py             # Concurrency test suite
├── users.db                       # User database (created at runtime)
└── server_IT24102872.log          # Server activity log (created at runtime)
```

### File Descriptions

| File | Purpose | Language |
|------|---------|----------|
| `server_2872.c` | Main server implementation with all core logic | C |
| `server_2872` | Compiled executable (generated after build) | Binary |
| `client_2872.py` | Interactive client for testing server | Python 3 |
| `test_concurrent.py` | Automated concurrent connection tester | Python 3 |
| `Makefile_2872` | Build configuration and targets | Makefile |
| `users.db` | SQLite-like user database with hashed passwords | Data |
| `server_IT24102872.log` | All server operations logged with timestamps | Log |

---

## 📦 Prerequisites

### System Requirements
- **OS:** Linux (tested on Ubuntu 20.04+)
- **Architecture:** x86_64 or ARM

### Dependencies

#### For Server (C)
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y build-essential libssl-dev

# Or install individual packages:
# - gcc (compiler)
# - libssl-dev (OpenSSL development libraries)
```

#### For Client (Python)
```bash
# Python 3.7+ (usually pre-installed)
python3 --version

# No additional Python packages required (uses only stdlib)
```

### Verify Installation
```bash
# Check GCC
gcc --version

# Check OpenSSL
openssl version

# Check Python
python3 --version
```

---

## 🔧 Installation & Building

### 1. Clone the Repository
```bash
git clone https://github.com/IT24102872/Secure-Multiprocessor-TCP-Application-Server.git
cd Secure-Multiprocessor-TCP-Application-Server
```

### 2. Build the Server

**Option A: Using Makefile (Recommended)**
```bash
make -f Makefile_2872
# Output: ✓ Build successful → ./server_2872
```

**Option B: Manual Compilation**
```bash
gcc -Wall -Wextra -g -o server_2872 server_2872.c -lssl -lcrypto
```

### 3. Verify Build
```bash
ls -la server_2872
# Should output: -rwxr-xr-x ... server_2872

./server_2872 --help  # (or just run it)
```

### 4. Set Up Data Directory
```bash
# The server creates this automatically, but you can pre-create it:
mkdir -p /home/lenovo/ie2102_assignment
chmod 755 /home/lenovo/ie2102_assignment
```

---

## 🚀 How to Run

### Starting the Server

**Option 1: Direct execution**
```bash
./server_2872
```

**Option 2: Using Makefile**
```bash
make -f Makefile_2872 run
```

**Option 3: Background execution (daemon)**
```bash
./server_2872 &
# Server output will print to console
```

### Expected Server Output
```
╔══════════════════════════════════════════╗
║  IE2102 Server   |  IT24102872           ║
║  Port  : 50872   |  SID  : 4102          ║
║  Hash  : PBKDF2-HMAC-SHA256 (100k iter) ║
║  Token : OpenSSL RAND_bytes              ║
╚══════════════════════════════════════════╝

[Parent] Forked PID=12345
[PID 12345] Client connected: 127.0.0.1:54321
```

### Starting the Client

**In a new terminal:**
```bash
# Make executable (if needed)
chmod +x client_2872.py

# Run the client
python3 client_2872.py
```

### Expected Client Output
```
╔══════════════════════════════════════════╗
║   IE2102 Client  |  IT24102872           ║
║   Server: 127.0.0.1:50872                ║
╠══════════════════════════════════════════╣
║  Commands:                               ║
║  REGISTER <user> <pass>                  ║
║  LOGIN    <user> <pass>                  ║
║  LOGOUT                                  ║
║  ECHO     <message with spaces>          ║
║  WHOAMI                                  ║
║  STATUS                                  ║
║  QUIT                                    ║
╚══════════════════════════════════════════╝

✓ Connected to 127.0.0.1:50872

client>> 
```

---

## 💻 Usage Guide

### Command Reference

#### 1. REGISTER (Create Account)
```bash
client>> REGISTER alice MyPassword123
server<< OK 201 SID:4102 Registered successfully.

client>> REGISTER alice MyPassword123
server<< ERR 409 SID:4102 Username already taken.
```

**Requirements:**
- Username: 3-20 alphanumeric characters or underscores
- Password: Minimum 6 characters

#### 2. LOGIN (Authenticate)
```bash
client>> LOGIN alice MyPassword123
server<< OK 200 SID:4102 Welcome alice! TOKEN:a1b2c3d4e5f6...

client>> LOGIN alice WrongPassword
server<< ERR 401 SID:4102 Wrong credentials. Attempt 1/3.
```

**Response includes:** Session token (valid for 300 seconds)

#### 3. LOGOUT (End Session)
```bash
client>> LOGOUT
server<< OK 200 SID:4102 Logged out successfully.
```

**Note:** Requires active login session

#### 4. ECHO (Echo Message)
```bash
client>> ECHO Hello, World! This is a test
server<< OK 200 SID:4102 Hello, World! This is a test

client>> ECHO
server<< ERR 400 SID:4102 Usage: ECHO <message>
```

**Note:** Requires login; returns full message including spaces

#### 5. WHOAMI (Current User)
```bash
client>> WHOAMI
server<< OK 200 SID:4102 You are: alice
```

**Note:** Requires login

#### 6. STATUS (Session Info)
```bash
client>> STATUS
server<< OK 200 SID:4102 User:alice TokenExpiresIn:280s
```

**Note:** Shows seconds until token expiration

#### 7. QUIT (Disconnect)
```bash
client>> QUIT
server<< OK 200 SID:4102 Goodbye!
Connection closed.
```

### Complete Session Example

```bash
# Terminal 1: Start Server
$ ./server_2872
╔══════════════════════════════════════════╗
║  IE2102 Server   |  IT24102872           ║
...

# Terminal 2: Start Client
$ python3 client_2872.py

client>> REGISTER john SecurePass123
server<< OK 201 SID:4102 Registered successfully.

client>> LOGIN john SecurePass123
server<< OK 200 SID:4102 Welcome john! TOKEN:7f8e9a1b2c3d...

client>> WHOAMI
server<< OK 200 SID:4102 You are: john

client>> ECHO Welcome to the secure server!
server<< OK 200 SID:4102 Welcome to the secure server!

client>> STATUS
server<< OK 200 SID:4102 User:john TokenExpiresIn:295s

client>> LOGOUT
server<< OK 200 SID:4102 Logged out successfully.

client>> QUIT
server<< OK 200 SID:4102 Goodbye!
```

---

## 🏗️ Architecture & Design

### System Architecture

```
┌─────────────────────────────────────────────┐
│         Main Server Process (Parent)        │
│   • Listens on port 50872                   │
│   • Accepts incoming connections            │
│   • fork() creates child for each client    │
│   • Reaps zombie processes (SIGCHLD)        │
└─────────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ↓           ↓           ↓
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Client #1    │ │ Client #2    │ │ Client #3    │
│ (PID 12345)  │ │ (PID 12346)  │ │ (PID 12347)  │
│              │ │              │ │              │
│ • Recv buf   │ │ • Recv buf   │ │ • Recv buf   │
│ • Session    │ │ • Session    │ │ • Session    │
│ • Rate limit │ │ • Rate limit │ │ • Rate limit │
│ • Lockout    │ │ • Lockout    │ │ • Lockout    │
└──────────────┘ └──────────────┘ └──────────────┘
        ↓               ↓               ↓
┌──────────────────────────────────────────────┐
│   Shared Resources (Thread-Safe)             │
│   • users.db (with flock)                    │
│   • server_IT24102872.log (with flock)       │
│   • /home/lenovo/ie2102_assignment/          │
└──────────────────────────────────────────────┘
```

### Message Protocol

#### Request Format
```
LEN:<payload_length>\n
<payload>
```

**Example:**
```
LEN:34
REGISTER alice MyPassword123
```

#### Response Format
```
LEN:<payload_length>\n
{OK|ERR} <code> SID:4102 <message>
```

**Examples:**
```
LEN:42
OK 200 SID:4102 Welcome alice! TOKEN:a1b2c3d4e5f6...

LEN:51
ERR 401 SID:4102 Wrong credentials. Attempt 1/3.
```

### Data Flow Diagram

```
Client                          Server
  │                               │
  ├──── TCP SYN ─────────────────→│
  │                               │
  ├──────── ACK ─────────────────→│
  │                          (fork child)
  │                               │
  ├── LEN:30\nREGISTER alice... ──→│
  │                               │ (hash password)
  │                               │ (write to users.db)
  │←─ LEN:42\nOK 201... ───────────┤
  │                               │
  ├── LEN:28\nLOGIN alice ... ────→│
  │                               │ (verify password)
  │                               │ (generate token)
  │←─ LEN:70\nOK 200 TOKEN:... ────┤
  │                               │
  ├── LEN:20\nECHO hello ────────→│
  │                               │ (check session)
  │←─ LEN:30\nOK 200 hello... ─────┤
  │                               │
  ├── LEN:10\nQUIT ──────────────→│
  │                               │ (exit child)
  │←─ LEN:30\nOK 200 Goodbye! ────┤
  │                               │
  └──── TCP FIN ─────────────────→│
```

### Session Management

```c
typedef struct {
    char   token[TOKEN_LEN+1];     // 64-char hex string (32 bytes random)
    char   username[64];            // Username (max 63 chars)
    time_t last_active;             // Unix timestamp of last request
    int    valid;                   // 1 if session active, 0 otherwise
} Session;
```

**Lifecycle:**
1. **LOGIN** → Generate token, set valid=1, record timestamp
2. **REQUEST** → Update last_active on each command
3. **TIMEOUT** → If (now - last_active) > 300s, expire session
4. **LOGOUT** → Clear session, set valid=0

---

## 🔐 Security Features

### Password Security
- **Algorithm:** PBKDF2-HMAC-SHA256
- **Iterations:** 100,000 (prevents rainbow tables)
- **Salt:** 16 random bytes (cryptographically generated)
- **Storage Format:** `<salt_hex>$<hash_hex>` (1024 bytes per entry max)

```c
// Example stored password
7f8e9a1b2c3d4e5f$a1b2c3d4e5f6...7f8e9a1b (128 hex chars total)
```

### Token Security
- **Generation:** OpenSSL RAND_bytes (cryptographically secure)
- **Length:** 64 hex characters (32 bytes random data)
- **Validation:** Exact match verification
- **Expiration:** 300 seconds (5 minutes) of inactivity

### Attack Protection

| Attack | Defense | Implementation |
|--------|---------|-----------------|
| **Brute-force** | Account lockout (3 failures → 300s lockout) | `fail_count` tracking, `locked` flag |
| **Rate limiting** | Max 10 requests/second per client | `req_count` with 1-second windows |
| **Token reuse** | Expiry on inactivity | `last_active` timestamp check |
| **Concurrent DB access** | File locking (flock) | Exclusive/shared locks on users.db |
| **Buffer overflow** | Payload size validation | `plen > MAX_PAYLOAD` check |
| **Malformed frames** | Protocol validation | `LEN:` header validation, frame draining |

### Database Locking Strategy

```c
// Read (shared lock)
FILE *f = fopen(USER_DB, "r");
lock_file(f, 0);  // LOCK_SH
// ... read operations ...
unlock_file(f);
fclose(f);

// Write (exclusive lock)
FILE *f = fopen(USER_DB, "a");
lock_file(f, 1);  // LOCK_EX
// ... write operations ...
unlock_file(f);
fclose(f);
```

---

## 📋 Protocol Specification

### Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK - Successful operation | LOGIN, ECHO |
| 201 | Created - Resource created | REGISTER |
| 400 | Bad Request - Invalid format | Malformed command |
| 401 | Unauthorized - Auth required/failed | Not logged in, wrong password |
| 403 | Forbidden - Access denied | Account locked |
| 404 | Not Found - Unknown command | Undefined command |
| 409 | Conflict - Resource exists | Username already taken |
| 413 | Payload Too Large | Payload > 4096 bytes |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Server Error | DB write failure |

### Command Grammar

```
REGISTER <username> <password>
LOGIN    <username> <password>
LOGOUT
ECHO     [message with spaces]
WHOAMI
STATUS
QUIT
```

**Rules:**
- Commands are case-sensitive (REGISTER, LOGIN, etc.)
- Arguments are space-separated
- ECHO captures everything after "ECHO " (preserves spaces)
- Newlines embedded in payload are not supported
- Max message length: 4096 bytes

---

## 🧪 Testing

### Concurrent Connection Test

Run the included test suite to verify server handles multiple simultaneous clients:

```bash
# Terminal 1: Start server
./server_2872

# Terminal 2: Run concurrent test
python3 test_concurrent.py
```

**Output:**
```
Testing concurrent connections...
[Client 0] Connected
[Client 1] Connected
[Client 2] Connected
[Client 3] Connected
[Client 4] Connected
All clients registered successfully
All clients logged in
Sending echo commands...
✓ All concurrent operations completed
```

### Manual Testing Checklist

```bash
# 1. Registration test
REGISTER testuser TestPass123   # Should succeed (201)
REGISTER testuser TestPass456   # Should fail with 409

# 2. Login test
LOGIN testuser TestPass123      # Should succeed with token (200)
LOGIN testuser WrongPass        # Should fail (401)

# 3. Session test
LOGIN user1 pass1
WHOAMI                          # Should show user1
(wait 5+ minutes)
ECHO test                       # Should fail with 401 (expired)

# 4. Rate limiting test
ECHO test
ECHO test
... (10x total in 1 second)
ECHO test                       # Should fail with 429

# 5. Lockout test
LOGIN attacker pass1            # Attempt 1 (401)
LOGIN attacker pass2            # Attempt 2 (401)
LOGIN attacker pass3            # Attempt 3 (401)
LOGIN attacker pass4            # Should fail with 403 (locked)
(wait 5+ minutes)
LOGIN attacker pass1            # Should work again
```

---

## 📊 Logging

All server operations are logged to `server_IT24102872.log`:

```
[2024-12-13 10:30:15] IP:127.0.0.1:54321 PID:12345 USER:NONE CMD:CONNECT RESULT:OK
[2024-12-13 10:30:20] IP:127.0.0.1:54321 PID:12345 USER:NONE CMD:REGISTER RESULT:OK
[2024-12-13 10:30:25] IP:127.0.0.1:54321 PID:12345 USER:alice CMD:LOGIN RESULT:OK
[2024-12-13 10:30:30] IP:127.0.0.1:54321 PID:12345 USER:alice CMD:ECHO RESULT:OK
[2024-12-13 10:30:35] IP:127.0.0.1:54321 PID:12345 USER:alice CMD:LOGOUT RESULT:OK
[2024-12-13 10:30:40] IP:127.0.0.1:54321 PID:12345 USER:NONE CMD:QUIT RESULT:OK
```

**Log Format:**
```
[YYYY-MM-DD HH:MM:SS] IP:<client_ip>:<port> PID:<process_id> USER:<username> CMD:<command> RESULT:<status>
```

---

## 🐛 Troubleshooting

### Server Won't Start

**Error:** `bind: Address already in use`
```bash
# Solution: Wait 60s or kill process using port 50872
lsof -i :50872
kill -9 <PID>

# Or restart with SO_REUSEADDR (already enabled)
```

**Error:** `Permission denied` (opening users.db)
```bash
# Solution: Check permissions on /home/lenovo/ie2102_assignment/
sudo mkdir -p /home/lenovo/ie2102_assignment
sudo chown $USER:$USER /home/lenovo/ie2102_assignment
chmod 755 /home/lenovo/ie2102_assignment
```

### Client Connection Issues

**Error:** `✗ Cannot connect to 127.0.0.1:50872`
```bash
# Solution 1: Verify server is running
ps aux | grep server_2872

# Solution 2: Check if port is listening
netstat -tuln | grep 50872

# Solution 3: Check firewall
sudo ufw allow 50872  (if using ufw)
```

### Build Errors

**Error:** `openssl/evp.h: No such file or directory`
```bash
# Solution: Install OpenSSL development libraries
sudo apt-get install libssl-dev
```

**Error:** `undefined reference to PKCS5_PBKDF2_HMAC`
```bash
# Solution: Link against libcrypto
gcc -lssl -lcrypto -o server_2872 server_2872.c
```

### Session Timeout Issues

**Issue:** Getting "Session expired" after short inactivity
```
This is expected behavior - tokens expire after 300s (5 minutes) of inactivity.
To keep session alive: Send STATUS or WHOAMI commands to refresh timestamp
```

### Database Corruption

**Issue:** Getting "Server DB error" (500)
```bash
# Solution: Backup and recreate database
mv users.db users.db.bak
# Restart server - new database will be created
```

### Multiple Clients Getting Rate Limited

**Issue:** "Too many requests" (429) with single client
```
This is a per-connection limit, not global. Each client gets 10 req/sec.
If multiple clients hit rate limit, they're independent - normal behavior.
```

---

## 📈 Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| **Concurrent Clients** | Unlimited | Limited by system resources (file descriptors, memory) |
| **Max Request Size** | 4096 bytes | Configurable via MAX_PAYLOAD |
| **Session Timeout** | 300s | 5 minutes of inactivity |
| **Password Hash Time** | ~100ms | PBKDF2 with 100k iterations |
| **Token Generation** | ~1ms | Using OpenSSL RAND_bytes |
| **Rate Limit** | 10 req/s | Per client connection |
| **Lockout Duration** | 300s | Auto-unlock after 5 minutes |

---

## 🔍 Code Structure

### Main Components

**server_2872.c** (648 lines)
- **Lines 1-69:** Configuration constants
- **Lines 71-155:** Receive buffer implementation (handles multiple messages)
- **Lines 157-189:** Utility functions (hex conversion, directory creation)
- **Lines 191-205:** Logging functions
- **Lines 207-213:** Signal handlers
- **Lines 215-270:** Cryptographic functions (PBKDF2, token generation)
- **Lines 272-291:** Database helper functions
- **Lines 293-336:** User registration/verification
- **Lines 338-353:** Response formatting
- **Lines 355-586:** Client handler (main command processing loop)
- **Lines 588-647:** Main server loop (accept, fork)

**client_2872.py** (116 lines)
- **Lines 1-12:** Module setup and constants
- **Lines 14-18:** Command sending with LEN framing
- **Lines 20-59:** Response reading with LEN parsing
- **Lines 61-74:** Banner display
- **Lines 76-115:** Main interactive loop

---

## 📝 Configuration

Edit these constants in `server_2872.c` to customize:

```c
#define PORT             50872      // Server port
#define SID              "4102"     // Station ID
#define TOKEN_TIMEOUT    300        // Session timeout (seconds)
#define LOCKOUT_DURATION 300        // Account lockout duration (seconds)
#define MAX_FAIL         3          // Failed login attempts before lockout
#define RATE_LIMIT       10         // Requests per second per client
#define MAX_PAYLOAD      4096       // Maximum message size (bytes)
#define PBKDF2_ITER      100000     // Password hash iterations
#define DATA_DIR         "/home/lenovo/ie2102_assignment"  // Data directory
```

Then rebuild:
```bash
make -f Makefile_2872 clean
make -f Makefile_2872
```

---

## 📚 References

- [RFC 793 - TCP Protocol](https://tools.ietf.org/html/rfc793)
- [OpenSSL EVP Functions](https://www.openssl.org/docs/man1.1.1/man3/EVP_PKEY_keygen.html)
- [PBKDF2 (RFC 2898)](https://tools.ietf.org/html/rfc2898)
- [POSIX Process Management](https://pubs.opengroup.org/onlinepubs/9699919799/functions/fork.html)
- [Socket Programming Guide](https://beej.us/guide/bgnet/)

---

## 🎓 Learning Outcomes

This project demonstrates:

✅ **Network Programming**
- TCP socket creation and management
- Connection handling with accept()
- Non-blocking I/O patterns
- Protocol design and framing

✅ **System Programming**
- Multi-process architecture with fork()
- Signal handling (SIGCHLD)
- File locking (flock)
- Process lifecycle management

✅ **Security**
- Cryptographic password hashing (PBKDF2)
- Secure random generation
- Rate limiting and brute-force protection
- Session management

✅ **Software Engineering**
- Error handling and validation
- Logging and debugging
- Code organization and documentation
- Build automation (Makefile)

---

## 📄 License

This project is part of the IE2102 Network Programming module assignment for university coursework.

---

## 👤 Author

**Student ID:** IT24102872  
**Module:** IE2102 - Network Programming  
**Institution:** [University Name]  
**Date:** December 2024

---

## 🤝 Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review the [Protocol Specification](#protocol-specification)
3. Check server logs: `cat server_IT24102872.log`
4. Verify system requirements in [Prerequisites](#prerequisites)

---

**Last Updated:** December 13, 2024  
**Version:** 1.0 (Final)  
**Status:** Production Ready
