Lamonte Server
==============

How to run these apps on developer's machine
--------------------------------------------

1. Install Postgres.app [http://postgresapp.com](http://postgresapp.com)
2. Install Python 2.7.10 and virtualenvwrapper
3. Install brew
4. Install redis, run `redis-server`
5. Install node.js
6. Create lamonte virtual env, workon lamonte
7. `pip install -r r.txt`
8. Run lamonet_server by executing `./run`
9. Run lamonte_node_server by executing `./run`
10. Open [http://192.168.1.100:9998/](http://192.168.1.100:9998/) in browser (`open http://192.168.1.100:9998/`) 

How to run these apps on server machine
---------------------------------------

Install optional pip packages from `or.txt`

Production setup is more complicated and involves nginx and reverse-proxy configuration

