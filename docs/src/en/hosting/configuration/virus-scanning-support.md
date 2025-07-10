# 🛡️ Virus Scanning (Optional)

Notivae supports **optional virus scanning** for uploaded files. This feature is designed to improve security in environments where users can upload arbitrary attachments — especially in multi-user or publicly accessible deployments.

## ✅ Overview

Virus scanning is **disabled by default** and only activates if the following two environment variables are set:

```env
CLAMAV_HOST=<host>
CLAMAV_PORT=<port>
```

When both are defined, Notivae will attempt to connect to the ClamAV service. If the connection fails at runtime while virus scanning is enabled, **file uploads will be rejected** for safety.

## 🔧 When to Enable Virus Scanning

You should enable virus scanning when:

- Notivae is hosted on a **public-facing server**
- You allow **guest access via shared links**
- You're running Notivae in an **enterprise or shared environment**
- You want defense against **known malware or trojan file uploads**

It’s typically **not necessary** for:
- Local, private deployments
- Environments where all users are trusted

## 🔍 How It Works

When enabled:
- Uploaded attachments are streamed to disk
- Once stored, the file is scanned using the ClamAV service
- If a threat is detected, the file is immediately deleted and the upload fails with an error
- Clean files proceed as normal

## 🐳 Docker Compose Setup

To enable virus scanning, add the ClamAV service to your `docker-compose.yml`:

```yaml
services:
  clamav:
    image: clamav/clamav:stable_base
    restart: unless-stopped
    volumes:
      - clamav-db:/var/lib/clamav  # persists virus signature database

volumes:
  clamav-db:
```

This image automatically checks for virus database updates **once per day**.

## ⚠️ Resource Requirements

ClamAV requires a **significant amount of RAM** to function properly. According to official documentation:

- Minimum recommended: **3 GB RAM**
- Optimal: **4 GB+ RAM**, depending on signature database and traffic

You should not enable virus scanning on hosts with limited memory or swap space unless you're confident in available resources.

## 🧪 Testing Virus Scanning

To verify that virus scanning is active and working, you can use the **EICAR test file**, a harmless file designed to trigger antivirus systems.

Download or create it using the official test string: <https://www.eicar.org/download-anti-malware-testfile/>

Upload this file to Notivae. If scanning is active, it will be rejected with a message like:

```
Virus detected: Eicar-Test-Signature
```

This confirms that your scanner integration is functional.
