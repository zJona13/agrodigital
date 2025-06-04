import json
from decimal import Decimal
import datetime

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        
        if isinstance(obj, datetime.date):
            return obj.strftime('%D-%M-%Y')
        
        return super(CustomJSONEncoder).default(obj)