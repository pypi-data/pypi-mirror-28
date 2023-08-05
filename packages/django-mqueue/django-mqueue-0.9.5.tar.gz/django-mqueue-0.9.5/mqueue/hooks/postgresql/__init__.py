import os
from mqueue.conf import DOMAIN
from mqueue.hooks import postgresql


def save(event, conf):
    params = ["-a="+conf["addr"]]
    params.append('-du="'+conf["user"]+'"')
    params.append('-p="'+conf["password"]+'"')
    params.append('-d="'+conf["database"]+'"')
    params.append('-t="'+conf["table"]+'"')
    params.append('-n="'+event.name+'"')
    params.append('-c="'+event.event_class+'"')
    params.append('-ct="'+str(event.content_type)+'"')
    params.append('-dm="'+DOMAIN+'"')
    obj_pk = 0
    if event.obj_pk is not None:
        obj_pk = event.obj_pk
    params.append("-o="+str(obj_pk))
    user = ""
    if event.user is not None:
        user = event.user.username
    params.append('-u="'+user+'"')
    params.append('-ur="'+event.url+'"')
    params.append('-au="'+event.admin_url+'"')
    params.append('-no="'+event.notes+'"')
    params.append('-r="'+event.request+'"')
    pth = os.path.dirname(postgresql.__file__)
    cmd = pth+"/run "+str.join(" ", params)
    os.system(cmd)
