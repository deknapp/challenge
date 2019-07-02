# Contains tools to read in the file.
import os
import struct
import sys

# gets a string type from the byte value
def get_type(byte):
  if byte == 0x00:
    return 'Debit'
  elif byte == 0x01:
    return 'Credit'
  elif byte == 0x02:
    return 'StartAutopay'
  elif byte == 0x03:
    return 'EndAutopay'
  else:
    print('ERROR: invalid byte for type ' + byte) 

# Returns dictionary of records
def read_file(file_name):
  handle = open(file_name, 'rb')
  file_content = handle.read() 
  version = file_content[4]
  num_records = int.from_bytes(file_content[5:9]) 
  records = {}
  debit_total = 0
  credit_total = 0
  num_autopays_started = 0
  num_autopays_ended = 0 
  for i in range(10:13:len(file_content)):
    record_type = get_type(file_content[i])
    
  
  print 'Total amount in dollars of debits: ' + debit_total 
  print 'Total amount in dollars of credits: ' + credit_total
  print 'Total number of autopays started: ' + num_autopays_started
  print 'Total number of autopays ended: ' + num_autopays_ended
  print 'Balance of user ID 2456938384156277127: ' + user_balance
