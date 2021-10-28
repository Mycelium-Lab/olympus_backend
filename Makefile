run-db:
	docker run --name olympus -p 5432:5432 -e POSTGRES_PASSWORD=mysuperpassword -e POSTGRES_DB=olympus -v ${PWD}/db_data:/var/lib/postgresql/data -d postgres
	