import hashlib
from decimal import Decimal 

class CommonUtils:
    def MD5(input):
        return hashlib.md5(input.encode('ascii')).hexdigest()
    
    def amount(input):
        return Decimal("%.2f"%float(input))