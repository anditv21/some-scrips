#!/bin/bash

# Database credentials
USER=""
PASSWORD=""
DATABASE=""

# Backup path
BACKUP_PATH="/var/db-backups"

# Date format for file name
DATE=$(date +"%Y-%m-%d_%H-%M-%S")

# Run mysqldump
mysqldump -u $USER -p$PASSWORD $DATABASE > "$BACKUP_PATH/${DATABASE}_backup_$DATE.sql"

# Optional: Remove backups older than 7 days
find $BACKUP_PATH -type f -name "*.sql" -mtime +7 -exec rm {} \;
