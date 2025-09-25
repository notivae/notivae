# @icon:clipboard-list Requirements

This page outlines the minimum and recommended requirements for deploying and running **Notivae**. These requirements vary depending on your intended usage, number of users, and system workload.

## @icon:wrench Prerequisites

Notivae is deployed exclusively using **Docker** and **Docker Compose**. Ensure both are installed and functioning on your host system before proceeding with the [installation](./installation/index.md).

## @icon:cpu CPU

Notivae is designed to run on **low-powered hardware**, making it suitable for self-hosted deployments and lightweight environments. However, the **actual CPU requirements depend on the number of users and the expected workload**.

Workload is influenced by factors such as:
- The number of concurrent users
- User activity (e.g., real-time collaboration, editing, and viewing frequency)
- Document complexity and size
- Usage of features like version history or media embedding

For small teams or personal use, a single-core virtual CPU (vCPU) should be sufficient. For larger teams or public-facing instances, allocate more CPU resources to maintain performance under load.


## @icon:memory-stick Memory (RAM)

- **Minimum**: 512MB  
- **Recommended**: 1GB or more for better performance

Memory usage grows with the number of active users and document interactions. High concurrency, frequent edits, or large documents will increase memory demand.


## @icon:save Disk Requirements

Disk performance can impact both the responsiveness and reliability of your Notivae instance.

- **Storage Type**: SSDs are strongly recommended over HDDs for faster read/write operations, especially under load.
- **Storage Capacity**: The required disk space depends on:
  - The number of users
  - The volume and size of stored notes
  - Any embedded content or attachments

Plan for growth and monitor usage over time to avoid disruptions.


## Other Dependencies

### @icon:globe Dedicated Domain or Sub-domain  
A dedicated domain or sub-domain (e.g., `notivae.example.com`) is **only required for public-facing deployments**, but it is **strongly recommended** even for internal or limited-use setups.

Without a proper domain:
- Some features like **link-sharing** may not work reliably
- **Authentication providers** often require a valid domain for redirect URIs and session handling
- Cross-device or remote access may be limited or problematic

While technically optional in private network environments, using a domain helps ensure full feature compatibility and smoother operation.

### @icon:fingerprint Authentication Provider  
Authentication is **required** in Notivae to associate documents and data with individual user accounts. By default, Notivae includes a built-in authentication system using email or username and password.  

Alternatively, Notivae can integrate with external authentication providers for single sign-on (SSO) or centralized user management. Supported providers include:
- OAuth2 providers (e.g., GitHub, GitLab, Discord)
- Any identity provider that supports OpenID Connect (OIDC)


## Additional Recommendations

- **HTTPS Support**: Use TLS/SSL certificates for encrypted traffic (strongly recommended, especially for public deployments).
- **Persistent Storage**: Ensure that your storage backend is reliable and backed up regularly. Document data and user metadata should be durable.
- **Reverse Proxy**: Set up a reverse proxy (e.g., Nginx, Caddy, or Traefik) to manage routing, SSL termination, and headers.
- **Monitoring and Logging**: Set up basic logging and metrics collection to track performance, detect issues early, and plan scaling.
