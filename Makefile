db-up:
	docker run -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=dough -p 5432:5432 --name dough -d postgres

wait-for-db:
	@echo "Waiting for database to be ready..."
	@sleep 5

unit-test: db-up wait-for-db
	cd backend && pytest
	docker stop dough
	docker rm dough
