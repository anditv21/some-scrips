#!/bin/bash

# Database credentials
USER=""
PASSWORD=""
DATABASE=""

# Backup path
BACKUP_PATH="/var/db-backups"

# Date format for file name
DATE=$(date +"%Y-%m-%d_%H-%M-%S")

mkdir -p "$BACKUP_PATH"

mysqldump --single-transaction --quick --lock-tables=false -u "$USER" -p"$PASSWORD" "$DATABASE" > "$BACKUP_PATH/${DATABASE}_backup_$DATE.sql"

# Check if dump was successful
if [ $? -eq 0 ]; then
    echo "Backup successful: $BACKUP_PATH/${DATABASE}_backup_$DATE.sql"
else
    echo "Backup failed!" >&2
    exit 1
fi


exit 0
