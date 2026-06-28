.PHONY: help migrate apply serve serve_admin env deploy-dev

.DEFAULT_GOAL := help

help:  ## Show this help message
	@echo "GeoCities Project Management Commands:"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

deploy-dev:  ## Build, push, and deploy to dev with yoink
	./deploy-dev.sh

env:  ## Create .env file from example
	cp .env.example .env
	@echo "Created .env file from example. Edit it if needed."

migrate:  ## Create migrations for sites app
	uv run python manage.py makemigrations

apply:  ## Apply migrations for sites app
	uv run python manage.py migrate

serve:  ## Run development server on port 3009
	uv run python manage.py runserver 3012

shell:  ## Open Django shell
	uv run python manage.py shell

createsuperuser:  ## Create superuser
	uv run python manage.py createsuperuser

reset_db:  ## Reset database (delete and recreate)
	rm -f db.sqlite3
	uv run python manage.py migrate
	uv run python manage.py createsuperuser

erd:  ## Generate ERD diagram
	uv run python -m django_diagram --settings=core.settings --output=erd_gen.md


# backup:
# 	pg_dump --dbname=postgresql://postgres@192.168.1.114:5430/geocities_v2 \
# 		--format=custom \
# 		--file=/nas_geocities/backups/database/django/geocities_v2_$$(date +%Y%m%d_%H%M%S).psql.backup

# backup:
# 	uv run python manage.py dbbackup --database default

# list_backups:
# 	uv run python manage.py listbackups --database default

# restore:
# 	uv run python manage.py dbrestore --database default --noinput --verbosity 1 --input-filename default-mint-vm-2026-01-10-220528.psql.bin 

# housekeeping:
# 	uv run python manage.py housekeeping all

# stats:
# 	uv run python manage.py stats_snapshot

# check_page_http_status:
# 	uv run python manage.py check_urls --index-only --cache-source restorativland --processes 10 --batch-size 10

# check_page_http_status_show_status:
# 	uv run python manage.py check_urls --show-status --cache-source restorativland  --processes 10 --batch-size 10

# update_site_cache_found_flag:
# 	uv run python manage.py update_site_cache_found_flag