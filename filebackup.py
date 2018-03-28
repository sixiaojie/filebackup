#!/usr/bin/env python
#coding:utf8

from config import root_backup,servers_config
import time, os,sys
from multiprocessing import Process,Pool,current_process

today = time.strftime('%Y-%m-%d')
mouth = time.strftime('%Y-%m')
flog = open('%s/log/%s.log' %(root_backup,today),'a')

def log(msg):
    tm = time.strftime('%Y-%m-%d %H:%M:%S')
    print >>sys.stderr,"[%s] %s" % (tm,msg)
    print >>flog, "[%s] %s" % (tm,msg)

def getLocalDir(ip,name,local):
    return "%s/%s-%s/%s" %(root_backup, name, ip, local)

def backupServer(server_config):
    print server_config
    name = server_config['name']
    log('%s:  server %s  start backup' %(current_process().name,name))
    rsync_opt = ' -avz --progress -e "ssh -p %s -o StrictHostKeyChecking=no -o PreferredAuthentications=publickey -o ConnectTimeout=3"' %(server_config['port'])
    if server_config["delete"]:
	opts = " --delete"
    else:
	opts = ""
    for item in server_config['sync']:
	if type(item) is not dict or not item.get('remote') or not item.get('local'):
		log('%s is failed,parameter is error' %(name))
		raise Exception("invalid config: missing remote/local")
	if item.get('exclude'):
		rsync_opt += " "+item.get('exclude')
	if item.get('delete',None):
		rsync_opt += " --delete"	
	elif item.get('delete',None) is False:
		rsync_opt += ""
	else:
		rsync_opt += opts
	localdir = getLocalDir(server_config['ip'],server_config['name'],item['local'])
	try:
		os.makedirs(localdir)
	except:
		if os.path.isdir(localdir):
			pass
		else:
			raise Exception("%s is't exist" %(localdir))
	cmd = "rsync %s 'root'@'%s':%s %s" %(rsync_opt, server_config['ip'], item['remote'], localdir)
	log('%s' %(cmd))
	ret = os.system(cmd)
	if ret != 0:
		raise Exception('backup failed for '+name)
	log("%s: backupserver %s ok" %(current_process().name,name))

def print_help():
	name = sys.argv[0]
	print >>sys.stderr,"""
Usage:
    %s list                             list available config
    %s backup [comma-separated list]    backup all or specified
        e.g. %s backup web4,web5
    """ % (name, name, name)
	sys.exit(1)	

def process_pool(configs,pool_num=3):
    try:
	print "start"
	pool = Pool(processes = pool_num)
	length = len(configs)
	for i in range(length):
		server_config = configs[i]
		pool.apply(backupServer,(server_config,))
	pool.close()
	pool.join()
    except Exception,e:
	print e
	log(e)
		
	
 
if __name__ == "__main__":
	if len(sys.argv) <2:
		print_help()
	else:
		action = sys.argv[1]
	if action not in ["list","backup"]:
		print_help()
        pool = Pool(processes = 3)
        length = len(servers_config)
        for i in range(length):
                server_config = servers_config[i]
                pool.apply_async(backupServer,(server_config,))
        pool.close()
        pool.join()
	log('backup finished')
