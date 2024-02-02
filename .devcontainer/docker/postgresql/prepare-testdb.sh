
#!/bin/bash

psql -U postgres -c 'SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid();'

createdb -U postgres -T postgres test_postgres
createdb -U postgres -T postgres test_geonode
createdb -U postgres -T postgres test_geonode_data

psql -U postgres -d test_geonode -c 'CREATE EXTENSION IF NOT EXISTS postgis;'
psql -U postgres -d test_geonode_data -c 'CREATE EXTENSION IF NOT EXISTS postgis;'
