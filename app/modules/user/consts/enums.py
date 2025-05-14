from enum import Enum


class ControllerPath(str, Enum):
    me = "/me"
    referrals = "/my_referrals"
