
from dotenv import load_dotenv
load_dotenv('.env')

from .novaPasta import criarPasta
from .transformar import transformar, mover
from .ACLs import set_acl,defaultACLs,setAclWay