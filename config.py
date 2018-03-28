#!/usr/bin/env python
#coding:utf8
root_backup="/data/backup"

servers_config=[
	{
	 "name":"ldap-test",
	 "ip":"10.105.58.226",
	 "port": 36000,
	 "sync": [
		{"remote":"/var/log/zabbix/","local":"zabbix/","exclude":"","delete":True},
		{"remote":"/var/log/httpd","local":"httpd/","exclude":""},
	],
	 "delete":True,
	},
        {
         "name":"Snipe-IT-test",
         "ip":"10.1.0.22",
         "port": 36000,
         "sync": [
                {"remote":"/var/log/zabbix/","local":"zabbix/","exclude":"","delete":False},
        ],
         "delete":True,
        }
]
