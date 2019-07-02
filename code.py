# Contains tools to read in the file.
import os
import struct
import sys

MAGIC_USER_ID = 2456938384156277127

def read_file(file_name):
  handle = open(file_name, 'rb')
  file_content = handle.read() 
  version = file_content[4]
  num_records = int.from_bytes(file_content[5:9], byteorder='big') 
  
  debit_total = 0
  credit_total = 0
  num_autopays_started = 0
  num_autopays_ended = 0 
  i = 0
  
  for record in range(num_records): 
    record_type = file_content[i]
    timestamp = int.from_bytes(file_content[i+1:i+5])
    user_id = int.from_bytes(file_content[i+5:i+13])    
    if user_id == MAGIC_USER_ID:
      if record_type == 0x01 or record_type == 0x00:
        user_balance += int.from_bytes(file_content[i+13:i+21], byteorder='big')
    if record_type == 0x01:
      dollar_amount = float.from_bytes(file_content[i+13:i+21], byteorder='big')
      credit_total += dollar_amount
      i += 21
    elif record_type == 0x00:
      dollar_amount = float.from_bytes(file_content[i+13:i+21], byteorder='big')
      debit_total += dollar_amount
      i += 21
    elif record_type == 0x02:
      num_autopays_started += 1
      i += 13
    elif record_type == 0x03:
      num_autopays_ended += 1
      i += 13
    else:
      print('ERROR: invalid record type ' + record_type)
      exit() 
  print 'Total amount in dollars of debits: ' + debit_total 
  print 'Total amount in dollars of credits: ' + credit_total
  print 'Total number of autopays started: ' + num_autopays_started
  print 'Total number of autopays ended: ' + num_autopays_ended
  print 'Balance of user ID 2456938384156277127: ' + user_balance

test_file_name = './test_files/txnlog.dat'
read_file(test_file_name)
