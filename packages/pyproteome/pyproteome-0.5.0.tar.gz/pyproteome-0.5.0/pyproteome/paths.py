"""
This module tracks the path to user data files. Developers can override paths
here when using a custom data hierarchy.
"""

import os

BASE_DIR = os.path.abspath("..")
BCA_ASSAY_DIR, CAMV_OUT_DIR, CAMV_SESS_DIR, MS_SEARCHED_DIR, \
    MS_RAW_DIR, SCRIPTS_DIR = (None,) * 6


def set_base_dir(path):
    global BCA_ASSAY_DIR, CAMV_OUT_DIR, CAMV_SESS_DIR, MASCOT_XML_DIR, \
        MS_SEARCHED_DIR, MS_RAW_DIR, SCRIPTS_DIR

    BCA_ASSAY_DIR = os.path.join(path, "BCA Protein Assays")
    CAMV_OUT_DIR = os.path.join(path, "CAMV Output")
    CAMV_SESS_DIR = os.path.join(path, "CAMV Sessions")
    MS_SEARCHED_DIR = os.path.join(path, "MS Searched")
    MS_RAW_DIR = os.path.join(path, "MS RAW")
    SCRIPTS_DIR = os.path.join(path, "Scripts")


set_base_dir(BASE_DIR)
