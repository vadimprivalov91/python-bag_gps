CREATE TABLE IF NOT EXISTS `push_notifications_gcmdevice` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	varchar ( 255 ),
	`active`	bool NOT NULL,
	`date_created`	datetime,
	`device_id`	UNSIGNED BIG INT,
	`registration_id`	text NOT NULL,
	`user_id`	integer,
	FOREIGN KEY(`user_id`) REFERENCES `lamonte_core_luser`(`id`)
);
CREATE TABLE IF NOT EXISTS `push_notifications_apnsdevice` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	varchar ( 255 ),
	`active`	bool NOT NULL,
	`date_created`	datetime,
	`device_id`	char ( 32 ),
	`registration_id`	varchar ( 64 ) NOT NULL UNIQUE,
	`user_id`	integer,
	FOREIGN KEY(`user_id`) REFERENCES `lamonte_core_luser`(`id`)
);
CREATE TABLE IF NOT EXISTS `lamonte_core_luser` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`is_admin`	bool NOT NULL,
	`password`	varchar ( 128 ) NOT NULL,
	`last_login`	datetime,
	`email`	varchar ( 255 ) NOT NULL UNIQUE,
	`is_active`	bool NOT NULL,
	`is_user_add_api_account`	bool NOT NULL,
	`lat`	real,
	`lon`	real,
	`name`	varchar ( 256 )
);
INSERT INTO `lamonte_core_luser` VALUES (1,1,'pbkdf2_sha256$20000$MPECWXfjQ0wu$oTN0ZgNaNPrwwEWi57h5esuiyJqioEU41RWGdjmcuew=','2018-06-27 08:53:31.330000','admin@admin.com',1,0,NULL,NULL,NULL);
CREATE TABLE IF NOT EXISTS `lamonte_core_latestdevicedataentry` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`created`	datetime NOT NULL,
	`data`	text NOT NULL,
	`imei`	bigint,
	`timestamp`	integer,
	`lat`	real,
	`lon`	real,
	`speed`	real,
	`coarse`	real,
	`cell_id`	integer,
	`battery`	real,
	`altitude`	real,
	`temperature`	real,
	`wifi_ssid_1`	varchar ( 32 ) NOT NULL,
	`wifi_ssid_2`	varchar ( 32 ) NOT NULL,
	`wifi_ssid_3`	varchar ( 32 ) NOT NULL,
	`wifi_ssid_4`	varchar ( 32 ) NOT NULL,
	`wifi_ssid_5`	varchar ( 32 ) NOT NULL,
	`wifi_mac_id_1`	varchar ( 64 ) NOT NULL,
	`wifi_mac_id_2`	varchar ( 64 ) NOT NULL,
	`wifi_mac_id_3`	varchar ( 64 ) NOT NULL,
	`wifi_mac_id_4`	varchar ( 64 ) NOT NULL,
	`wifi_mac_id_5`	varchar ( 64 ) NOT NULL,
	`gsm_signal_strength`	varchar ( 64 ),
	`hdop`	varchar ( 64 ),
	`num_of_satellite_used`	varchar ( 64 ),
	`gps_valid`	integer,
	`bag_id`	integer,
	FOREIGN KEY(`bag_id`) REFERENCES `lamonte_core_bag`(`id`)
);
CREATE TABLE IF NOT EXISTS `lamonte_core_devicedataentry` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`created`	datetime NOT NULL,
	`data`	text NOT NULL,
	`altitude`	real,
	`battery`	real,
	`cell_id`	integer,
	`coarse`	real,
	`imei`	bigint,
	`lat`	real,
	`lon`	real,
	`speed`	real,
	`temperature`	real,
	`timestamp`	integer,
	`wifi_mac_id_1`	varchar ( 64 ) NOT NULL,
	`wifi_mac_id_2`	varchar ( 64 ) NOT NULL,
	`wifi_mac_id_3`	varchar ( 64 ) NOT NULL,
	`wifi_mac_id_4`	varchar ( 64 ) NOT NULL,
	`wifi_mac_id_5`	varchar ( 64 ) NOT NULL,
	`wifi_ssid_1`	varchar ( 32 ) NOT NULL,
	`wifi_ssid_2`	varchar ( 32 ) NOT NULL,
	`wifi_ssid_3`	varchar ( 32 ) NOT NULL,
	`wifi_ssid_4`	varchar ( 32 ) NOT NULL,
	`wifi_ssid_5`	varchar ( 32 ) NOT NULL,
	`bag_id`	integer,
	`gps_valid`	integer,
	`gsm_signal_strength`	varchar ( 64 ),
	`hdop`	varchar ( 64 ),
	`num_of_satellite_used`	varchar ( 64 ),
	FOREIGN KEY(`bag_id`) REFERENCES `lamonte_core_bag`(`id`)
);
CREATE TABLE IF NOT EXISTS `lamonte_core_contact` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	varchar ( 1024 ) NOT NULL,
	`iso`	varchar ( 3 ) NOT NULL,
	`phone`	varchar ( 1024 ) NOT NULL,
	`e164Phone`	varchar ( 1024 ) NOT NULL,
	`formattedPhone`	varchar ( 1024 ) NOT NULL,
	`bag_id`	integer NOT NULL,
	FOREIGN KEY(`bag_id`) REFERENCES `lamonte_core_bag`(`id`)
);
CREATE TABLE IF NOT EXISTS `lamonte_core_bag` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	varchar ( 1024 ) NOT NULL,
	`owner_id`	integer NOT NULL,
	`imei`	bigint NOT NULL UNIQUE,
	`geo_fence`	real NOT NULL,
	`tracking`	bool NOT NULL,
	`lat`	real,
	`lon`	real,
	`altitude`	real,
	`speed`	real,
	`distance`	real,
	`battery`	real NOT NULL,
	`charging`	bool NOT NULL,
	`image`	varchar ( 100 ),
	`nearby`	bool NOT NULL,
	`macid`	varchar ( 250 ) UNIQUE,
	FOREIGN KEY(`owner_id`) REFERENCES `lamonte_core_luser`(`id`)
);
CREATE TABLE IF NOT EXISTS `django_session` (
	`session_key`	varchar ( 40 ) NOT NULL,
	`session_data`	text NOT NULL,
	`expire_date`	datetime NOT NULL,
	PRIMARY KEY(`session_key`)
);
INSERT INTO `django_session` VALUES ('8nvv7akwz6n4w77l2qd0kofgpyl5cf05','MWY4ZWUwYzJmMGJlZmVkNmZmOWRhODA1OWQ2YWE4MDdlM2ExNGQ1ODp7Il9hdXRoX3VzZXJfaGFzaCI6ImViMmRmZWQ0MWNhYTIxNDEwY2E1YzY3NWFjMDFkYzNiNjI4YmRmZTIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2018-07-10 15:04:52.820000');
INSERT INTO `django_session` VALUES ('2wt2ddgkdp78mvj1iudsm1f8enrn7pli','MWY4ZWUwYzJmMGJlZmVkNmZmOWRhODA1OWQ2YWE4MDdlM2ExNGQ1ODp7Il9hdXRoX3VzZXJfaGFzaCI6ImViMmRmZWQ0MWNhYTIxNDEwY2E1YzY3NWFjMDFkYzNiNjI4YmRmZTIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2018-07-11 08:53:31.377000');
CREATE TABLE IF NOT EXISTS `django_migrations` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`app`	varchar ( 255 ) NOT NULL,
	`name`	varchar ( 255 ) NOT NULL,
	`applied`	datetime NOT NULL
);
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-06-26 14:44:21.791000');
INSERT INTO `django_migrations` VALUES (2,'contenttypes','0002_remove_content_type_name','2018-06-26 14:44:21.952000');
INSERT INTO `django_migrations` VALUES (3,'auth','0001_initial','2018-06-26 14:44:22.080000');
INSERT INTO `django_migrations` VALUES (4,'auth','0002_alter_permission_name_max_length','2018-06-26 14:44:22.211000');
INSERT INTO `django_migrations` VALUES (5,'auth','0003_alter_user_email_max_length','2018-06-26 14:44:22.292000');
INSERT INTO `django_migrations` VALUES (6,'auth','0004_alter_user_username_opts','2018-06-26 14:44:22.474000');
INSERT INTO `django_migrations` VALUES (7,'auth','0005_alter_user_last_login_null','2018-06-26 14:44:22.655000');
INSERT INTO `django_migrations` VALUES (8,'auth','0006_require_contenttypes_0002','2018-06-26 14:44:22.738000');
INSERT INTO `django_migrations` VALUES (9,'lamonte_core','0001_initial','2018-06-26 14:44:23.510000');
INSERT INTO `django_migrations` VALUES (10,'admin','0001_initial','2018-06-26 14:44:23.766000');
INSERT INTO `django_migrations` VALUES (11,'authtoken','0001_initial','2018-06-26 14:44:24.098000');
INSERT INTO `django_migrations` VALUES (12,'lamonte_core','0002_auto_20160812_1041','2018-06-26 14:44:24.869000');
INSERT INTO `django_migrations` VALUES (13,'lamonte_core','0003_auto_20160818_1030','2018-06-26 14:44:25.588000');
INSERT INTO `django_migrations` VALUES (14,'lamonte_core','0004_bag_macid','2018-06-26 14:44:25.910000');
INSERT INTO `django_migrations` VALUES (15,'lamonte_core','0005_luser_name','2018-06-26 14:44:26.185000');
INSERT INTO `django_migrations` VALUES (16,'push_notifications','0001_initial','2018-06-26 14:44:26.402000');
INSERT INTO `django_migrations` VALUES (17,'sessions','0001_initial','2018-06-26 14:44:26.617000');
CREATE TABLE IF NOT EXISTS `django_content_type` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`app_label`	varchar ( 100 ) NOT NULL,
	`model`	varchar ( 100 ) NOT NULL,
	UNIQUE(`app_label`,`model`)
);
INSERT INTO `django_content_type` VALUES (1,'lamonte_core','luser');
INSERT INTO `django_content_type` VALUES (2,'lamonte_core','bag');
INSERT INTO `django_content_type` VALUES (3,'lamonte_core','contact');
INSERT INTO `django_content_type` VALUES (4,'lamonte_core','latestdevicedataentry');
INSERT INTO `django_content_type` VALUES (5,'lamonte_core','devicedataentry');
INSERT INTO `django_content_type` VALUES (6,'admin','logentry');
INSERT INTO `django_content_type` VALUES (7,'auth','permission');
INSERT INTO `django_content_type` VALUES (8,'auth','group');
INSERT INTO `django_content_type` VALUES (9,'contenttypes','contenttype');
INSERT INTO `django_content_type` VALUES (10,'sessions','session');
INSERT INTO `django_content_type` VALUES (11,'push_notifications','gcmdevice');
INSERT INTO `django_content_type` VALUES (12,'push_notifications','apnsdevice');
INSERT INTO `django_content_type` VALUES (13,'authtoken','token');
CREATE TABLE IF NOT EXISTS `django_admin_log` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`action_time`	datetime NOT NULL,
	`object_id`	text,
	`object_repr`	varchar ( 200 ) NOT NULL,
	`action_flag`	smallint unsigned NOT NULL,
	`change_message`	text NOT NULL,
	`content_type_id`	integer,
	`user_id`	integer NOT NULL,
	FOREIGN KEY(`content_type_id`) REFERENCES `django_content_type`(`id`),
	FOREIGN KEY(`user_id`) REFERENCES `lamonte_core_luser`(`id`)
);
CREATE TABLE IF NOT EXISTS `authtoken_token` (
	`key`	varchar ( 40 ) NOT NULL,
	`created`	datetime NOT NULL,
	`user_id`	integer NOT NULL UNIQUE,
	PRIMARY KEY(`key`),
	FOREIGN KEY(`user_id`) REFERENCES `lamonte_core_luser`(`id`)
);
INSERT INTO `authtoken_token` VALUES ('f9884151dbb24c656b2c72a223ec58570f6af1bc','2018-06-26 15:03:43.621000',1);
CREATE TABLE IF NOT EXISTS `auth_permission` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`content_type_id`	integer NOT NULL,
	`codename`	varchar ( 100 ) NOT NULL,
	`name`	varchar ( 255 ) NOT NULL,
	FOREIGN KEY(`content_type_id`) REFERENCES `django_content_type`(`id`),
	UNIQUE(`content_type_id`,`codename`)
);
INSERT INTO `auth_permission` VALUES (1,1,'add_luser','Can add User');
INSERT INTO `auth_permission` VALUES (2,1,'change_luser','Can change User');
INSERT INTO `auth_permission` VALUES (3,1,'delete_luser','Can delete User');
INSERT INTO `auth_permission` VALUES (4,2,'add_bag','Can add Bag');
INSERT INTO `auth_permission` VALUES (5,2,'change_bag','Can change Bag');
INSERT INTO `auth_permission` VALUES (6,2,'delete_bag','Can delete Bag');
INSERT INTO `auth_permission` VALUES (7,3,'add_contact','Can add Contact Assigned for Bag');
INSERT INTO `auth_permission` VALUES (8,3,'change_contact','Can change Contact Assigned for Bag');
INSERT INTO `auth_permission` VALUES (9,3,'delete_contact','Can delete Contact Assigned for Bag');
INSERT INTO `auth_permission` VALUES (10,4,'add_latestdevicedataentry','Can add Latest Device Data Entry');
INSERT INTO `auth_permission` VALUES (11,4,'change_latestdevicedataentry','Can change Latest Device Data Entry');
INSERT INTO `auth_permission` VALUES (12,4,'delete_latestdevicedataentry','Can delete Latest Device Data Entry');
INSERT INTO `auth_permission` VALUES (13,5,'add_devicedataentry','Can add Device Data Entry');
INSERT INTO `auth_permission` VALUES (14,5,'change_devicedataentry','Can change Device Data Entry');
INSERT INTO `auth_permission` VALUES (15,5,'delete_devicedataentry','Can delete Device Data Entry');
INSERT INTO `auth_permission` VALUES (16,6,'add_logentry','Can add log entry');
INSERT INTO `auth_permission` VALUES (17,6,'change_logentry','Can change log entry');
INSERT INTO `auth_permission` VALUES (18,6,'delete_logentry','Can delete log entry');
INSERT INTO `auth_permission` VALUES (19,7,'add_permission','Can add permission');
INSERT INTO `auth_permission` VALUES (20,7,'change_permission','Can change permission');
INSERT INTO `auth_permission` VALUES (21,7,'delete_permission','Can delete permission');
INSERT INTO `auth_permission` VALUES (22,8,'add_group','Can add group');
INSERT INTO `auth_permission` VALUES (23,8,'change_group','Can change group');
INSERT INTO `auth_permission` VALUES (24,8,'delete_group','Can delete group');
INSERT INTO `auth_permission` VALUES (25,9,'add_contenttype','Can add content type');
INSERT INTO `auth_permission` VALUES (26,9,'change_contenttype','Can change content type');
INSERT INTO `auth_permission` VALUES (27,9,'delete_contenttype','Can delete content type');
INSERT INTO `auth_permission` VALUES (28,10,'add_session','Can add session');
INSERT INTO `auth_permission` VALUES (29,10,'change_session','Can change session');
INSERT INTO `auth_permission` VALUES (30,10,'delete_session','Can delete session');
INSERT INTO `auth_permission` VALUES (31,11,'add_gcmdevice','Can add GCM device');
INSERT INTO `auth_permission` VALUES (32,11,'change_gcmdevice','Can change GCM device');
INSERT INTO `auth_permission` VALUES (33,11,'delete_gcmdevice','Can delete GCM device');
INSERT INTO `auth_permission` VALUES (34,12,'add_apnsdevice','Can add APNS device');
INSERT INTO `auth_permission` VALUES (35,12,'change_apnsdevice','Can change APNS device');
INSERT INTO `auth_permission` VALUES (36,12,'delete_apnsdevice','Can delete APNS device');
INSERT INTO `auth_permission` VALUES (37,13,'add_token','Can add token');
INSERT INTO `auth_permission` VALUES (38,13,'change_token','Can change token');
INSERT INTO `auth_permission` VALUES (39,13,'delete_token','Can delete token');
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`group_id`	integer NOT NULL,
	`permission_id`	integer NOT NULL,
	FOREIGN KEY(`group_id`) REFERENCES `auth_group`(`id`),
	UNIQUE(`group_id`,`permission_id`),
	FOREIGN KEY(`permission_id`) REFERENCES `auth_permission`(`id`)
);
CREATE TABLE IF NOT EXISTS `auth_group` (
	`id`	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	varchar ( 80 ) NOT NULL UNIQUE
);
CREATE INDEX IF NOT EXISTS `push_notifications_gcmdevice_e8701ad4` ON `push_notifications_gcmdevice` (
	`user_id`
);
CREATE INDEX IF NOT EXISTS `push_notifications_gcmdevice_9379346c` ON `push_notifications_gcmdevice` (
	`device_id`
);
CREATE INDEX IF NOT EXISTS `push_notifications_apnsdevice_e8701ad4` ON `push_notifications_apnsdevice` (
	`user_id`
);
CREATE INDEX IF NOT EXISTS `push_notifications_apnsdevice_9379346c` ON `push_notifications_apnsdevice` (
	`device_id`
);
CREATE INDEX IF NOT EXISTS `lamonte_core_latestdevicedataentry_cb9bb33f` ON `lamonte_core_latestdevicedataentry` (
	`bag_id`
);
CREATE INDEX IF NOT EXISTS `lamonte_core_latestdevicedataentry_6fbbfd04` ON `lamonte_core_latestdevicedataentry` (
	`imei`
);
CREATE INDEX IF NOT EXISTS `lamonte_core_devicedataentry_cb9bb33f` ON `lamonte_core_devicedataentry` (
	`bag_id`
);
CREATE INDEX IF NOT EXISTS `lamonte_core_devicedataentry_6fbbfd04` ON `lamonte_core_devicedataentry` (
	`imei`
);
CREATE INDEX IF NOT EXISTS `lamonte_core_contact_cb9bb33f` ON `lamonte_core_contact` (
	`bag_id`
);
CREATE INDEX IF NOT EXISTS `lamonte_core_contact_b068931c` ON `lamonte_core_contact` (
	`name`
);
CREATE INDEX IF NOT EXISTS `lamonte_core_bag_b068931c` ON `lamonte_core_bag` (
	`name`
);
CREATE INDEX IF NOT EXISTS `lamonte_core_bag_5e7b1936` ON `lamonte_core_bag` (
	`owner_id`
);
CREATE INDEX IF NOT EXISTS `lamonte_core_bag_515fb6f6` ON `lamonte_core_bag` (
	`nearby`
);
CREATE INDEX IF NOT EXISTS `lamonte_core_bag_18799662` ON `lamonte_core_bag` (
	`tracking`
);
CREATE INDEX IF NOT EXISTS `django_session_de54fa62` ON `django_session` (
	`expire_date`
);
CREATE INDEX IF NOT EXISTS `django_admin_log_e8701ad4` ON `django_admin_log` (
	`user_id`
);
CREATE INDEX IF NOT EXISTS `django_admin_log_417f1b1c` ON `django_admin_log` (
	`content_type_id`
);
CREATE INDEX IF NOT EXISTS `auth_permission_417f1b1c` ON `auth_permission` (
	`content_type_id`
);
CREATE INDEX IF NOT EXISTS `auth_group_permissions_8373b171` ON `auth_group_permissions` (
	`permission_id`
);
CREATE INDEX IF NOT EXISTS `auth_group_permissions_0e939a4f` ON `auth_group_permissions` (
	`group_id`
);
COMMIT;
