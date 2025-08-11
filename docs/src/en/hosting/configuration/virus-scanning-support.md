# @lucide:shield Virus Scanning (Optional)

Notivae supports **optional virus scanning** for uploaded files. This feature is designed to improve security in environments where users can upload arbitrary attachments — especially in multi-user or publicly accessible deployments.

## When to Enable Virus Scanning

You should **enable virus scanning** if:

- Notivae is hosted on a **public-facing server**
- You allow **guest access** via shared links
- You're running Notivae in an **enterprise or shared multi-user environment**
- You want basic protection against **known malware and trojans**

You can likely **skip enabling scanning** if:

- You're running a **local or private deployment**
- **All users are trusted**, such as in internal dev/test setups

## Environment Variables

Virus scanning is **disabled by default**. To enable it, you must set the `CLAMAV_SERVER` environment variable:

```dotenv
CLAMAV_SERVER=
CLAMAV_PORT=3310
```

Once defined, Notivae will attempt to connect to the ClamAV service. If the connection fails while virus scanning is enabled, **file uploads will be rejected** as a safety precaution.

## How to Set Up Virus Scanning

To enable virus scanning, add the ClamAV service to your `docker-compose.yml`:

::: code-group
```yaml [docker-compose.yml]
services:
  clamav:
    image: clamav/clamav:stable_base
    restart: unless-stopped
    volumes:
      - clamav-db:/var/lib/clamav  # persists virus signature database

volumes:
  clamav-db:
```
:::

Then configure your `.env` file with the required environment variables:

::: code-group
```dotenv [.env]
CLAMAV_SERVER=clamav
CLAMAV_PORT=3310
```
:::

The official ClamAV image automatically updates its virus definitions **once per day**.

> [!WARNING]
> During these updates, ClamAV may temporarily use **up to double its normal RAM** due to *concurrent reloading*. This mechanism allows scans to continue while ClamAV reloads its updated virus signatures, but it means memory usage can spike briefly. Ensure your host system has enough headroom to handle these periodic memory peaks, especially on low-memory environments.

### 🔍 Testing Virus Scanning

To confirm virus scanning is active and functioning, use the **EICAR test file** — a harmless file designed to trigger antivirus systems:

- Download or create it using the string provided at: <https://www.eicar.org/download-anti-malware-testfile/>
- Upload the file to Notivae

If the scanner is correctly integrated, the upload will be rejected with an error like:

```
Virus detected: Eicar-Test-Signature
```

This confirms scanning is working as expected.

## Resource Requirements

ClamAV requires a **significant amount of RAM** to function properly. According to official documentation:

- Minimum recommended: **3 GB RAM**
- Optimal: **4 GB+ RAM**, depending on signature database and traffic

You should not enable virus scanning on hosts with limited memory or swap space unless you're confident in available resources.

## How It Works

When enabled:
- Any uploaded attachments are scanned using the ClamAV service
- If a threat is detected, the file is immediately deleted and the upload fails with an error
- Clean files proceed as normal
