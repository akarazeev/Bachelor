#!/bin/bash
createdb digitlabDB;
echo "create user digitlab with superuser password '12345678';" | psql digitlabDB;

python db_communication/init_db.py;

