run:
	docker compose up --remove-orphans 

test:
	docker compose -f docker-compose.test.yaml up --remove-orphans -d
#  wait for containers to start
	sleep 5
	docker exec -i jobboard chmod +x jobboard/tests/report.sh
	docker exec -i jobboard ./jobboard/tests/report.sh

ingest:
	docker compose up --remove-orphans -d
	docker exec -i jobboard python manage.py load-historical-jobs
