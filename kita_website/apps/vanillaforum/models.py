import MySQLdb
import md5

from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from selvbetjening.data.members.signals import user_created
from selvbetjening.data.members.signals import user_changed_password, user_changed_username

class VanillaForum:

    def __init__(self):
        self.db = MySQLdb.connect(host=settings.FORUM_DATABASE_HOST,
                                  user=settings.FORUM_DATABASE_USER,
                                  passwd=settings.FORUM_DATABASE_PASSWORD,
                                  db=settings.FORUM_DATABASE_NAME,
                                  use_unicode=True,
                                  charset='utf8')

    def prepare_password_for_forum(self, password):
        return md5.new(password.encode('utf-8')).hexdigest()

    def userExists(self, username):
        cursor = self.db.cursor()
        cursor.execute("SELECT Name FROM LUM_User where Name=%s", (username,))
        result = cursor.fetchone()

        return (result != None)

    def authenticateUser(self, username, password):
        cursor = self.db.cursor()
        cursor.execute("SELECT Name FROM LUM_User where Name=%s AND Password=%s", (username, md5.new(password.encode('utf-8')).hexdigest()))
        result = cursor.fetchone()
        cursor.close()

        return (result != None)

    def fetchUser(self, username):
        """
        Fetch the username, fist name, last name and email for a given user on the forum.
        The returend data are not filtered / escaped in any way, so be careful.

        returned index:: 0 : Username, 1 : First name, 2: Last name, 3: Email
        """
        cursor = self.db.cursor()
        cursor.execute("SELECT Name, FirstName, LastName, Email FROM LUM_User where Name=%s", (username, ))
        result = cursor.fetchone()
        cursor.close()

        # Lets trust the vanilla forum data, the forum should have escaped the data for html entities
        # Worst case: The data are shown in a form, where it is escaped, and later validated before it is saved in the database again.

        return result

    def createUser(self, Name, Password, Email, FirstName, LastName, RoleID=3, StyleID=None):
        """
        Password needs to be a MD5 hash. The RoleID is set to 3, (member) by default. StyleID must be 0, otherwise a very ugly forum is shown ;D
        Dammit, there are to many "magic" values in this system...

        """
        if not StyleID:
            StyleID = self.getLatestStyleID()

        cursor = self.db.cursor()
        cursor.execute("INSERT INTO LUM_User (Name, Password, Email, FirstName, LastName, RoleID, StyleID) VALUES (%s, %s, %s, %s, %s, %s, %s)", (Name, Password, Email, FirstName, LastName, RoleID, StyleID))
        cursor.close()

    def updateUser(self, OldUsername, Username, Password, Email, FirstName, LastName):
        cursor = self.db.cursor()
        cursor.execute("UPDATE LUM_User SET Name=%s, Password=%s, Email=%s, FirstName=%s, LastName=%s WHERE Name=%s",
                       (Username, md5.new(Password.encode('utf-8')).hexdigest(), Email, FirstName, LastName, OldUsername))
        cursor.close()

    def changeUserEmail(self, username, email):
        cursor = self.db.cursor()
        cursor.execute("UPDATE LUM_User SET Email=%s WHERE Name=%s", (email, username))
        cursor.close()

    def changeUserPassword(self, username, password):
        passwd = md5.new(password.encode('utf-8'))

        cursor = self.db.cursor()
        cursor.execute("UPDATE LUM_User SET Password=%s WHERE Name=%s", (passwd.hexdigest(), username))
        cursor.close()

    def changeUserUsername(self, old_username, new_username):
        cursor = self.db.cursor()
        cursor.execute("UPDATE LUM_User SET Name=%s WHERE Name=%s",
                       (new_username, old_username))
        cursor.close()

    def getLatestStyleID(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT StyleID FROM LUM_Style ORDER BY StyleID DESC LIMIT 1")

        result = cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return 0

# listen for new users
def new_user_listner(sender, **kwargs):
    instance = kwargs['instance']

    vanilla_forum = VanillaForum()
    vanilla_forum.createUser(instance.username,
                             vanilla_forum.prepare_password_for_forum(kwargs['clear_text_password']),
                             instance.email,
                             instance.first_name,
                             instance.last_name)

user_created.connect(new_user_listner)

# listen for users changing their password
def change_user_password_listner(sender, **kwargs):
    instance = kwargs['instance']

    vanilla_forum = VanillaForum()
    vanilla_forum.changeUserPassword(instance.username, kwargs['clear_text_password'])

user_changed_password.connect(change_user_password_listner)

# listen for user changing their username
def change_user_username_listener(sender, **kwargs):
    old_username = kwargs['old_username']
    new_username = kwargs['new_username']

    vanilla_forum = VanillaForum()
    vanilla_forum.changeUserUsername(old_username, new_username)

user_changed_username.connect(change_user_username_listener)