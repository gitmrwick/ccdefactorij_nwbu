#!/usr/bin/env python3

from datetime import datetime
from csv import reader
import pexpect
import subprocess

isodatetime = datetime.now().isoformat()
