import sys
import httplib
import urllib
from optparse import OptionParser

DEFAULT_HOST = '127.0.0.1:8124'
TIMEOUT = 10
DEFAULT_OUTPUTFILE = 'default.zip'

def get_sourcecode_from_clooca(outfile, host):
    hclient = httplib.HTTPConnection(host, timeout=TIMEOUT)
    username = raw_input("UserName:")
    password = raw_input("PassWord:")
    params = urllib.urlencode({'email': username, 'password': password})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "application/json, text/javascript, */*;"}
    hclient.request('POST','/login-to',params,headers)
    response = hclient.getresponse()
    print response.status, response.reason
    cookie = response.getheader('Set-Cookie')
    data = response.read()
    
    projectkey = raw_input("project key:")
    branch = raw_input("branch:")
    version = raw_input("version:")
    target = raw_input("target id:")
    """
    projectkey='40eb1aa6d615d6448ae08a1eea976050'
    branch='master'
    version='HEAD'
    target = 'uv4gnfk71'
    """
    headers = {"Cookie": cookie}
    hclient.request('GET','/ed-api/gen?key='+projectkey+'&branch='+branch+'&version='+version+'&selectedMenu=a&target_id='+target,'',headers)
    response = hclient.getresponse()
    print response.status, response.reason
    data = response.read()
    f = open(outfile, 'wb')
    f.write(data)
    f.close()
    hclient.close()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-o", "--output", dest="filename",
                  help="output filename", metavar="FILE")
    parser.add_option("-h", "--host", dest="host",
                  help='give host name. example:"www.clooca.com:8124"')
    (options, args) = parser.parse_args()
    if options.filename != None:
        filename = options.filename
    else:
        filename = DEFAULT_OUTPUTFILE
    if options.host != None:
        host = options.host
    else:
        host = DEFAULT_HOST
    path = sys.argv[0]
    print path+'/'+filename
    get_sourcecode_from_clooca(path+'/'+filename, host);
    