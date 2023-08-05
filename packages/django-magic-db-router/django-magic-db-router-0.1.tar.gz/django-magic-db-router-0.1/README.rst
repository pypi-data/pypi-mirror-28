
=====
Django-magic-db-router
=====

Django-magic-db-router is an app to allow Django system can auto pick random database for read/write, generally!

The key feature is we can use dedicated database for code block, this will usefull for transaction handler!


Quick start
-----------
1. Install the app:
	pip install django-magic-db-router

2. Config your settings file, for example:
	DJANGO_MAGIC_DB_ROUTER_READ_DB_LIST=['REPLICA1', 'REPLICA2', 'REPLICA3',]
	DJANGO_MAGIC_DB_ROUTER_WRITE_DB_LIST=['default',]
	DATABASE_ROUTERS = ['django_magic_db_router.DynamicDbRouter']	

3. For using dedicated database for code block, use: `in_database`
	with in_database(db_name, write=True):
		some_code()

========================================================================================
