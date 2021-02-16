from os import environ
from mysql.connector import connect, Connect

from os import environ


class MySqlDatabase():
    """
        Stores the credentials. They can be passed as non-keyword arguments or keywords arguments in the constructor.
        
        @kwargs:
            string: host -> hostname to database to connect
            string: port -> port to stabilish connection
            string: user -> user with required access level to app database
            string: password -> key to authenticate user and stabilish a connection to the DB
            string: use_aws_profile -> Override default profile with desired one
            string: use_aws_region -> Override default region with selected one
            enum: auth_method -> Specify how the user should login, possible values are:
                - AWS_SSM -> use an aws profile to access determined account parameter store
                - AWS_DDB -> use an aws profile to access determined account dynamo DB table
                - ENV_FILE -> use environment variables (MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD)
                - DEFAULT -> If no other method is specified, credentials are supposed to be passed as regular arguments
    """

    def __init__(self, host=None, port=None, user=None, password=None, **kwargs):
        """
             Stores the credentials. They can be passed as non-keyword arguments or keywords arguments.
        """

        if 'auth_method' in kwargs.keys():
            # Generates a auth mapping to link the correct auth method to its appropriate callback
            auth_methods = {
                'ENV_FILE': self.get_credentials_from_env_file,
                'AWS_DDB': self.get_credentials_from_dynamo,
                'AWS_SSEM': self.get_credentials_from_path
            }

            # If a valid authentication callback has been found, execute it (Note that the method executed here is defaulted. Any customized parameters must be run separately)
            auth_callback = auth_methods.get(kwargs['auth_method'], None)
            if auth_callback:
                auth_callback()
                return
                
            print(kwargs['auth_method'])

        # If other methods failed or no auth method has been provided, get credentials using its parameters
        self.credentials = {
            'user':user,
            'password':password,
            'host':host,
            'port':port,
        } 

    def get_credentials_from_env_file(self):
        self.credentials = {
            'user':environ['MYSQL_USER'],
            'password':environ['MYSQL_PASSWORD'],
            'host':environ['MYSQL_HOST'],
            'port':environ['MYSQL_PORT'],
        } 

    def get_credentials_from_path(self, custom_path='/DB/MYSQL'):
        pass

    def get_credentials_from_dynamo(self, custom_table_name="dynamo_parameters", custom_pk='DB_MYSQL'):
        pass

    def connect(self)-> Connect:
        """
            Estabilished a new connection to the database and returns the instance to that connection.
        """
        conn = connect(**self.credentials)
        
        return conn

    def test(self):
        query = """
            SELECT rolled_number, COUNT(rolled_number)
            FROM investopedia.megasena_historicalrecord
            GROUP BY rolled_number
            ORDER BY rolled_number
            LIMIT 10
        """

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute(query)
        print(cursor.fetchall())

    def close(self, conn: Connect):
        """
            Closes the connection to the database
        """
        conn.close()