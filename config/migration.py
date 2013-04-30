

def conf():
    return {
       # A mapping of connections avaiable to use for the migrations
       # These should be sqlalchemy connection strings
       'connections': { 'DEFAULT': 'mysql://root:@localhost/test'} 

        };
