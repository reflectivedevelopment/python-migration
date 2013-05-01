

def conf():
    return {
       # A mapping of connections avaiable to use for the migrations
       # These should be sqlalchemy connection strings
       'connections': { 'default': {
                            'database':'test',
                            'hostname':'localhost',
                            'username':'root',
                            'password':'',
                            'persistent':False,
                            }
                      } 

        };
