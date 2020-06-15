# FILE: database manager
# Manages the database by adding removing and updating the databases.

import sqlite3  # Import database interface
import hashlib # Hashing algorithms
import os # To generate the salt

# Current target to delete - deprecated for now
deletetarget: int = 0


# Used to add a new item to the database
# This also will call an Update to the UI which will load a new widget
# @param title: the title the user entered
# @param description: the description the user entered
# @param ConText: the caption the user entered
# @param image: the image URL that the user entered
# @param id: the id that the user entered
# @param ind: a string version of the id
# @param likes: number of current likes
def AddNewItem(title: str, description: str, ConText: str, image: str, id: int, ind: str, likes:int):
    sql = sqlite3.connect('content.db')
    c = sql.cursor()
    c.execute("""INSERT INTO content VALUES (?,?,?,?,?,?,?)""", (id, ind, title, description, image, ConText, likes,))
    sql.commit()
    sql.close()
    entries.append(Entry(description, title, ConText, image, id, ind, likes))


# This will remove an item from the database at the specified index
# @param index: The index of the item to remove
def RemoveItem(index):
    # Server Store of Entries
    sql = sqlite3.connect('content.db')
    c = sql.cursor()
    c.execute("""DELETE FROM content WHERE ind = (?)""", (index,))
    c.close()
    sql.commit()
    sql.close()
    # Local Store of Entries



# This will load the content initially to the user from the server.
# By creating new Objects
def LoadContent():
    sql = sqlite3.connect('content.db', timeout=5)
    c = sql.cursor()
    c.execute("""SELECT * FROM content""")
    result = c.fetchall()
    entries.clear()
    for i in result:
        NewEntry = Entry(i[3], i[2], i[5], i[4], i[0], i[1], i[6])
        entries.append(NewEntry)


# Object class which contains the neccessary infomation to create a new widget
class Entry():
    """ENTRY CLASS
    Class desc: A object class which when added will contain the data for an Entry.
    Instances of this class will be contained in array

    description (str): A brief description on the posted entry
    title (str): The title of the entry
    ConText (str): The subtitle of the image
    image (str): The image URL
    id (int): Object's id in relation to database
    ind (str): String version of the id
    likes (int): Number of likes
    """
    description: str
    title: str
    ConText: str
    image: str
    id: int
    ind: str
    likes: int

    # Object Constructor
    # Initialises the default values
    def __init__(self, description, title, ConText, image, id, ind, likes):
        self.description = description
        self.title = title
        self.ConText = ConText
        self.image = image
        self.id = id
        self.ind = ind
        self.likes = likes

# Function gets a string and encrypts it.
# @param password: the string to be encrypted
# @return str: the generated encrypted string
def Encrypt(password):
    salt = b'm\xe6%\x83,\xc1&\xa2\\s\x7fj\xb4\xfa\xcenZ&+\x7f\xe5\xbbx?/H\xe0\xabz-e\x0e'
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    return key


# Function Checks if the user credentials are valid
# @param username: username user entered
# @param password: password user entered
# @return bool: Was the username and password valid?
def CheckUser(username: str, password: str):
    sql = sqlite3.connect('login.db')
    c = sql.cursor()
    c.execute("""SELECT * FROM login WHERE Username == (?) AND Password == (?)""", (username, str(Encrypt(password)),))
    result = c.fetchone()
    print(str(Encrypt(password)))
    try:
        if result[1] == username:
            if str(result[2]) == str(Encrypt(password)):
                return True

    except:
        return False

# Function will add a new user to the login database
# @param Username: username the user entered
# @param Passowrd: Password the user entered
# @return bool: Was the user created successfully?
def NewUser(Username: str, Password: str):
    # try:
    sql = sqlite3.connect('login.db')
    c = sql.cursor()
    c.execute("""INSERT INTO login VALUES (?,?,?)""", (int(GetLoginLength()), Username, str(Encrypt(Password)),))
    sql.commit()
    sql.close()
    return True


# except:
# return False

# Gets the current length of the database
# @return int: length of the loggin database
def GetLoginLength():
    length: int = 0
    sql = sqlite3.connect('login.db')
    c = sql.cursor()
    c.execute("""SELECT * FROM login""")
    result = c.fetchall()
    for i in result: # could simplify
        length += 1
    return length

# Checks the key the user entered with the one on database
# @param key: the key the user entered
# @return bool: Was the key valid?
def CheckKey(key: str):
    try:
        sql = sqlite3.connect('key.db')
        c = sql.cursor()
        c.execute("""SELECT * FROM key WHERE key == (?)""", (key,))
        result = c.fetchone()
        if str(result[1]) == key:
            return True
        else:
            return False
    except:
        return False

# Gets the number of likes at specified index and adds 1 like to it.
# @param id: index of where to add like
def AddLike(id: int):
    sql = sqlite3.connect('content.db')
    c = sql.cursor()
    num = GetLikes(id)
    num = num + 1
    c.execute("""UPDATE content SET Likes = (?) WHERE id=(?)""", (num, id,))
    sql.commit()
    sql.close()

# Gets the current number of likes at a specified index in the database
# @param id: index of row in database
# @return int: number of likes at index
def GetLikes(id: int):
    sql = sqlite3.connect('content.db')
    c = sql.cursor()
    c.execute("""SELECT Likes FROM content WHERE id=(?)""", (id,))
    return int(c.fetchone()[0])

# List where the current entries are loaded into
# DECLARE entries AS LIST
entries = []


