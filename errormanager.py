import enum


# Class EErrorType Enumeration
# Used to help handle error events and display appropriate logging information in a format that the user can read.
# @type: Failed Password: When the password is invalid
# @type: Failed Username: When the username is invalid
# @type: Failed Key: When the admin key is invalid
# @type: Failed None: When an input or process returns nothing
# @type: Failed Confirm: When a process fails execution
class EErrorType(enum.Enum):
    FailedPassword = 0
    FailedUsername = 1
    FailedKey = 2
    FailedNone = 3
    FailedConfirm = 4


