def start_mongo_service():
    import subprocess
    from subprocess import call 
    status = subprocess.check_output("systemctl show -p ActiveState --value mongodb.service",
                                    shell=True,
                                    universal_newlines=True).strip()
    pwd='er'
    cmd='systemctl stop mongodb.service'
    
    if status == "active":
        call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)
        print('MONGO STOPED')
    else:
        print('MONGO IS NOT RUNNING')

start_mongo_service()