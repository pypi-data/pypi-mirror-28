"""Shared functionalities for the shleem package."""

import os


HOMEDIR = os.path.expanduser("~")
SHLEEM_DIR_NAME = '.shleem'
SHLEEM_DIR_PATH = os.path.join(HOMEDIR, SHLEEM_DIR_NAME)
os.makedirs(SHLEEM_DIR_PATH, exist_ok=True)

SHLEEM_CFG_FNAME = 'config.json'
SHLEEM_CFG_FPATH = os.path.join(SHLEEM_DIR_PATH, SHLEEM_CFG_FNAME)
