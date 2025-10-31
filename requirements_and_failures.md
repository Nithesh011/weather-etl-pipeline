
# Build failures & fixes (project log)

## 1) pip as root warning
**Message:** "You are running pip as root..."
**Fix:** Run pip install as the 'airflow' user in Dockerfile (follow Airflow docs). Resolved.

## 2) COPY requirements.txt failed
**Message:** COPY requirements.txt: file not found
**Fix:** Created requirements.txt in repo root and retried build. Resolved.

## 3) Java / PySpark compatibility
**Issue:** PySpark needs JDK
**Fix:** Installed OpenJDK 17 on VM and added to Docker image; set JAVA_HOME. Resolved.

## 4) Admin login invalid
**Issue:** created admin earlier, password mismatch
**Fix:** Deleted user and recreated using airflow users delete and users create. Resolved.

## 5) File path mismatches
**Issue:** scripts saved/expected files at different paths.
**Fix:** Standardized DATA_PATH to /opt/airflow/scripts inside container and updated DAG and scripts. Resolved.

## 6) Date mismatch (extract vs transform)
**Issue:** extract wrote yesterday's file but transform used today's date.
**Fix:** Both scripts now use (datetime.now() - timedelta(days=1)) for consistent filenames. Resolved.

## 7) Permissions
**Issue:** Airflow writing files may fail due to permissions.
**Fix:** Set dev-friendly permissions in Dockerfile (chmod 777) and mount repo read/write. For production, tighten permissions. Resolved.

## Final status
- Docker image built successfully.
- Airflow container runs.
- DAG weather_data_mumbai runs extract → transform → load successfully.
  
