from enum import Enum


class RoutersPath(str, Enum):
    me = "/me"
    referrals = "/my_referrals"
