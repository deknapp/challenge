# Contains tools to read in the file.
import os
import struct
import sys

def read_file(file_name):
  handle = open(file_name, 'rb')
  file_content = handle.read() 
  version = struct.unpack()  
 
 
