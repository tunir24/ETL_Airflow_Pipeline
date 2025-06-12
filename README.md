Set-Up Apache Airflow Ecosystem Using Astro

 -> Enable Windows Subsystem For Linux (WSL)
 -> Run command : wsl --update
       			  wsl --install --no-distribution
 -> Run Command Prompt as Administrator
 -> Run : winget install -e --id Astronomer.Astro
 -> Open Folder on VsCode
 -> Run command : astro dev init
 -> Create DAG & docker-compose.yaml 
 -> Run : astro dev start , having docker opened
(https://www.astronomer.io/docs/learn/get-started-with-airflow).
- Dockerfile: This file contains a versioned Astro Runtime Docker image that provides a differentiated Airflow experience. If you want to execute other commands or overrides at runtime, specify them here.
- include: This folder contains any additional files that you want to include as part of your project. It is empty by default.
- packages.txt: Install OS-level packages needed for your project by adding them to this file. It is empty by default.
- requirements.txt: Install Python packages needed for your project by adding them to this file. It is empty by default.
- plugins: Add custom or community plugins for your project to this file. It is empty by default.
- airflow_settings.yaml: Use this local-only file to specify Airflow Connections, Variables, and Pools instead of entering them in the Airflow UI as you develop DAGs in this project.


