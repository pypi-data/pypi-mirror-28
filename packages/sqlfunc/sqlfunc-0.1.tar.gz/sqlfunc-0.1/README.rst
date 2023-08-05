sqlfunc
=======

Clever stuff with SQL in __doc__

Features
--------

- In-memory or file-backed database (Sqlite)
- Post-process returned data
- User definded functions

Example
-------

Given this:

.. code:: python

    ''' CREATE TABLE IF NOT EXISTS users (
            userid   INTEGER PRIMARY KEY,
            username TEXT    UNIQUE NOT NULL,
            bcrypt   BLOB    NOT NULL
        );
    '''
    from sqlfunc import sqlinit, sqludf, sqlfunc
    
    __database__ = ':memory:' # default
    
    @sqludf
    def bcrypt_hash(password):
        # call to library here
        return b'$2b$12$.OjbRwRejxw92C89sA6JkOVrhmQzGsjoyCf1ofIN9hUNdHFufb3ty'
    
    @sqludf
    def bcrypt_verify(password, bcrypthash):
        # call to library here
        return True
    
    @sqlfunc
    def add_user(username, password):
        ''' INSERT OR IGNORE INTO $$$ (username, bcrypthash)
            VALUES (:username, bcrypt_hash(:password));
        '''
     
    @sqlfunc(post=lambda x: bool(list(x)))
    def login(username, password):
        ''' SELECT 1 FROM users
            WHERE username=:username
              AND bcrypt_verify(:password, bcrypt);
        '''
        
    sqlinit()

You can now do this:

.. code:: python

    >>> import example_users
    >>> example_users.add_user('root', 'password123')
    >>> example_users.login('root', 'secret')
    False
    >>> example_users.login('root', 'password123')
    True
    >>> example_users.list_users()
    ['root']
    >>> 'bcrypt_verify' in dir(example_users) # helper functions are NOT exported
    False

This library is MIT licensed.
