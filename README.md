endpoints: 
	
 	http://127.0.0.1:8000/api/docs/
	
	http://127.0.0.1:8000/api/<wallet_uuid>/
 
 	http://127.0.0.1:8000/api/<wallet_uuid>/operation/

Для тестирования параллельных запросов использовать sender.py
	
 	docker exec -it wallet sh
 	python sender.py


SELECT * from wallet;
                  id                  | account
--------------------------------------+---------
 2c0cea8c-7d88-4f5d-85a2-f1ab0c7de0f3 |  100.00
 7cab6001-74d7-4937-8b9b-b2f7da9060f8 |  400.00
 a058aaca-e0a7-4edf-8ea9-149dffe54ac6 |   52.52
 ac242451-cf2e-437d-bda2-905825406b27 |  200.00
 f828c13e-a976-48ed-a0ec-3286c4eb4585 |  300.00
