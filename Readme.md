# Cloud-Based Secure File Sharing System

## Overview

Cloud-Based Secure File Sharing System is a web application that enables users to securely upload, store, share, and download files through cloud storage. The system provides password-protected sharing links, secure authentication, and cloud-hosted storage using Supabase.

The project is built using Flask and deployed on Render, demonstrating cloud computing concepts such as cloud storage, web application deployment, secure file sharing, and database management.

---

## Features

* User Registration and Login
* Secure Session Management
* File Upload to Cloud Storage
* File Download from Cloud Storage
* Password-Protected File Sharing
* Unique Share Links
* Share Link Expiration
* Cloud Database Integration
* Responsive User Interface
* Public Cloud Deployment

---

## Technology Stack

### Frontend

* HTML
* CSS
* Jinja2 Templates

### Backend

* Python
* Flask

### Cloud Services

* Supabase Storage
* Supabase Database
* Render Hosting

### Security

* Password Hashing (Werkzeug)
* Secure Random Share Tokens
* Session-Based Authentication

---

## Project Architecture

User
↓
Flask Web Application
↓
Supabase Database
↓
Supabase Storage

---

## Working

### User Authentication

Users can register and log in securely. Passwords are hashed before storage.

### File Upload

Users upload files through the dashboard. Files are stored in Supabase Storage.

### File Download

Files are retrieved from cloud storage and delivered securely to users.

### Secure Sharing

Users generate password-protected sharing links.

Workflow:

1. User selects a file.
2. User enters a sharing password.
3. System generates a secure token.
4. Share link is created.
5. Recipient opens link.
6. Recipient enters password.
7. File is downloaded after successful verification.

---

## Security Features

* Password Hashing
* Secure Random Tokens
* Password-Protected Access
* Expiring Share Links
* Session Authentication
* Cloud-Based Secure Storage

---

## Deployment

Application deployed using:

* GitHub
* Render
* Supabase


