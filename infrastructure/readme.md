# bring it up
docker-compose up -d
# check the config
docker-compose config
# check the logs
docker-compose logs python-app 
docker-compose logs mysql 

#populate the dbs
docker-compose exec python-app python /app/db/order_repository_inttest.py
