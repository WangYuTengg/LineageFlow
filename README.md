# LineageFlow
Easily track data versions and lineage through the machine learning lifecycle.

## 𝌞 Table of Contents
- [About](#about)
    - [Problem Statement](#problem-statement)
    - [Motivation](#motivation)
    - [Target Audience](#target-audience)
    - [Value Proposition](#value-proposition)
    - [Tech Stack](#tech-stack)
    - [Architecture](#architecture)
- [Features](#features)
    - [Data Versioning](#data-versioning)
    - [Lineage Tracking](#lineage-tracking)
    - [Collaboration](#collaboration)
    - [Google Cloud Integration](#google-cloud-integration)
- [Roadmap for Scalability and Availability](#roadmap-for-scalability-and-availability)

## About
### <a name="problem-statement"></a>❓ Problem Statement
How can we develop a tool that tracks data versions and lineage through the machine learning lifecycle, helping data scientists understand how datasets have changed over time and how different versions of datasets affect model performance?

### <a name="motivation"></a>💡 Motivation
As datasets evolve, tracking their changes and understanding their impact on machine learning models becomes increasingly complex. LineageFlow aims to simplify this process by providing an intuitive tool for data versioning and lineage tracking, ensuring data manageability, quality, and reproducibility.

### <a name="target-audience"></a>🧑 Target Audience
- Data Scientists
- Machine Learning Engineers
- Data Engineers
- Organizations needing robust data management solutions

### <a name="value-proposition"></a>❗ Value Proposition
LineageFlow leverages Git-like semantics such as branches, commits, merges, and rollbacks to offer a familiar and powerful system for data versioning and lineage tracking. This approach allows users to manage, collaborate, and ensure the quality of their data throughout its lifecycle.

### <a name="tech-stack"></a>💻 Tech Stack
![React](https://img.shields.io/badge/React-%23061DAFB.svg?style=for-the-badge&logo=React&logoColor=white)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)
![Django](https://img.shields.io/badge/Django-%23092E20.svg?style=for-the-badge&logo=Django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/Postgres-%23316192.svg?style=for-the-badge&logo=PostgreSQL&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)

**Client**:
- React
- Vite

**Backend**:
- Django
- Django REST Framework

**Storage**:
- Supabase PostgresSQL for storing file object pointers
- Google Cloud Bucket for storing file objects

### <a name="architecture"></a>🔨 Architecture
![Architecture Diagram](https://github.com/WangYuTengg/LineageFlow/blob/main/architecture-diagram.jpg)

## Features
### <a name="data-versioning"></a>📂 Data Versioning
Aim:
- Enable users to track changes in their datasets using Git-like semantics.

*Features:*
- Branches, commits, merges, and rollbacks
- Blame functionality to identify the origin of each data change
- Ability to view datasets as they appeared before transformations

### <a name="lineage-tracking"></a>🗂 Lineage Tracking
Aim:
- Provide comprehensive tracking of data lineage to ensure reproducibility and quality.

*Features:*
- Detailed lineage graphs
- Visualization of data transformations
- Impact analysis of dataset changes on models

### <a name="collaboration"></a>🤝 Collaboration
Aim:
- Facilitate collaboration among data practitioners.

*Features:*
- Shared repositories for datasets
- Collaborative editing and version control
- Role-based access control

### <a name="google-cloud-integration"></a>☁️ Google Cloud Integration
Aim:
- Seamless integration with Google Cloud Storage for managing data.

*Features:*
- Direct storage and retrieval of data from Google Cloud Bucket
- Restore functionalities
- Scalable storage solutions

## Future Plans


## ✍🏻 Contributors
* [Jayden](https://github.com/MomPansy) - Fullstack
* [Wang Yu Teng](https://github.com/WangYuTengg) - Fullstack 
* [Pei Yee](https://github.com/heypeiyee) - Database, Backend

Feel free to customize the links and content as needed for your specific project.
