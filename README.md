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
    - [Database Design](#database-design)
- [Features](#features)
- [Future Plans](#roadmap-for-scalability-and-availability)
- [Challenges](#challenges-faced)
- [Contributors](#-contributors)

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
- Supabase PostgresSQL
- Google Cloud Storage

### <a name="architecture"></a>🔨 Architecture
![Architecture Diagram](https://github.com/WangYuTengg/LineageFlow/blob/main/assets/architecture-diagram.jpg)
- We store our actual objects and data in Google Cloud Storage, and pointers to the data in our Postgres SQL Database

### <a name='database-design'></a>🛠️ Database design
![Data Hierarchy Diagram](https://github.com/WangYuTengg/LineageFlow/blob/main/assets/data_hierarchy.jpg)
- In order to support data-versioning using Git-like semantics, we followed the above data hierarchy which sculpted our database schemas and design decisions.
- With this, we are able to implement version control when operations such as add, delete, and edit are done on the data.

<ul>
  <li>
    1. Adding Objects
    <br>
    <img src="https://github.com/WangYuTengg/LineageFlow/blob/main/assets/adding_objects.jpg" alt="Add Object Diagram">
  </li>
  <li>
    2. Deleting Objects
    <br>
    <img src="https://github.com/WangYuTengg/LineageFlow/blob/main/assets/deleting_objects.jpg" alt="Delete Object Diagram">
  </li>
  <li>
    3. Editing Objects
    <br>
    <img src="https://github.com/WangYuTengg/LineageFlow/blob/main/assets/editing_objects.jpg" alt="Edit Object Diagram">
  </li>
</ul>

## Current Features
- 
-
-
-
-
-

## Future Plans
-
-
-
-

## Challenges Faced
- 
- 
- 
-

## ✍🏻 Contributors
* [Jayden](https://github.com/MomPansy) - Fullstack
* [Wang Yu Teng](https://github.com/WangYuTengg) - Fullstack 
* [Pei Yee](https://github.com/heypeiyee) - Database, Backend