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
    - [Features](#features)
    - [Repositories](#repository)
    - [Objects view](#objects)
    - [Staging area](#staging)
    - [Branches](#branches)
    - [Commits](#commits)
    - [Settings](#settings)
- [Future Plans](#future-plans)
- [Challenges](#challenges-faced)
- [Contributors](#-contributors)

## About
### <a name="problem-statement"></a>❓ Problem Statement
How can we develop a tool that tracks data versions and lineage through the machine learning lifecycle, helping data scientists understand how datasets have changed over time and how different versions of datasets affect model performance?

### <a name="motivation"></a>💡 Motivation
As datasets evolve, tracking their changes and understanding their impact on machine learning models becomes increasingly complex. LineageFlow aims to simplify this process by providing an intuitive tool for data versioning and lineage tracking, ensuring data manageability, quality, and reproducibility. We strive to build a solid foundation, for everything data, ML & AI related. 

### <a name="target-audience"></a>🧑 Target Audience
- Data Scientists and Engineers
- Machine Learning Engineers
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
### <a name='repository'></a> Repositories
![Repositories Diagram](https://github.com/WangYuTengg/LineageFlow/blob/main/assets/repo-list.JPG)
- Simple user signup, login and auth flow
- View your repositories
- Create a new repository (with an option the repository to existing cloud bucket)

### <a name='objects'></a> Objects view
![Objects Diagram](https://github.com/WangYuTengg/LineageFlow/blob/main/assets/objects-page.JPG)
- View objects in file & folder structure
- Upload objects into repository (local files and folders) 
- Download/View/Delete objects

### <a name='staging'></a> Staging area
![Uncommitted Diagram](https://github.com/WangYuTengg/LineageFlow/blob/main/assets/uncommited-changes-page.JPG)
- Move to staging area before uncommitted changes are committed
- View changes before making them
- Enter a commit message

### <a name='branches'></a> Branches
![Branch Diagram](https://github.com/WangYuTengg/LineageFlow/blob/main/assets/branches-page.JPG)
- A single repository can have multiple branches
- Create branch from a parent branch
- Each branch has its own commit history, and data versioning

### <a name='commits'></a> Commits
![Commit Diagram](https://github.com/WangYuTengg/LineageFlow/blob/main/assets/commits-page.JPG)
- View detailed commit history of selected branch (files added/deleted/edited) in a timeline view
- Rollback/revert to a certain commit in history

### <a name='settings'></a> Settings
![Settings Diagram](https://github.com/WangYuTengg/LineageFlow/blob/main/assets/settings-page.JPG)
- Rename your repository
- Switch/rename default branch
- Delete your repository
- View collaborators

## Future Plans
- Immediate improvements to be made are: 
    - **Cloud Integration**: Incorporate other cloud buckets (e.g. AWS S3, Azure blob storage, CloudFare R2 etc.)
    - **Collaboration**: Enable collaboration through adding user roles, invites, branch merging etc.
    - **Deployment**: Deploy our product to quickly iterate based on real usage.

- The possibilities are endless:
    - **Feature Store**: Integrate a feature store to manage and share features across different machine learning models, ensuring consistency and reusability.
    - **Automated ML Pipeline**: Develop automated machine learning pipelines to streamline data preprocessing, model training, evaluation, and deployment, increasing efficiency and reducing manual intervention.
    - **Data Quality Monitoring**: Implement data quality monitoring and alerting systems to detect anomalies, ensuring data integrity and reliability throughout the machine learning lifecycle.

## Challenges Faced
- Designing the database correctly was most crucial and we should have spent more time on it, a lot of time was wasted on re-migrations because we realised our database schemas did not work.
- Integration with google cloud bucket proved to be technically difficult, facing issues such as authentication 
- Underestimated scope of project and faced time constraints

## ✍🏻 Contributors
* [Jayden](https://github.com/MomPansy) - Fullstack
* [Wang Yu Teng](https://github.com/WangYuTengg) - Fullstack 
* [Pei Yee](https://github.com/heypeiyee) - Database, Backend