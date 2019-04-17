from Helpers.SettingsHelper import settings
from Models.Auth.UserModel import UserModel


def CreateUserForAuth():
    user_name = settings['credentials']['user']
    user_pass = settings['credentials']['password']
    user = UserModel(user_name, user_pass)
    return user
