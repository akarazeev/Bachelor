import psycopg2
import db_queries
import os

db_queries.commit_query("db_communication/users_creation.txt")

db_queries.commit_query("db_communication/users_files_creation.txt")
