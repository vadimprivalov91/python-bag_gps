
Paul Brennan	2 May 2017
I've moved all old log files and software backups to /home/nt/backups.
Implemented lamonte_server backups and DB backups
	- Copies logs to /home/nt/backups then cat /dev/null
		- gunicorn.log
		- gunicorn.accesslog
		- debug.log
	- Backs up lamonte_server to backups
	- Cleans up old backups



