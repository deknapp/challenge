# Contains tools to read in the file.
import os
import struct
import sys

MAGIC_USER_ID = 2456938384156277127

DEBIT_TYPE = 0x01
CREDIT_TYPE = 0x00
AUTOPAY_START_TYPE = 0x02 
AUTOPAY_END_TYPE = 0x03 
AUTOPAY_RECORD_LENGTH = 13
TRANSACTION_RECORD_LENGTH = 21

def read_file(file_name):
  handle = open(file_name, 'rb')
  file_content = handle.read() 
  version = file_content[4]
  num_records = int.from_bytes(file_content[5:9], byteorder='big') 
  
  debit_total = 0
  credit_total = 0
  num_autopays_started = 0
  num_autopays_ended = 0 
  i = 4
  for record in range(num_records): 
    record_type = file_content[i]
    timestamp = int.from_bytes(file_content[i+1:i+5], byteorder='big')
    user_id = int.from_bytes(file_content[i+5:i+13], byteorder='big')    
    dollar_amount = 0 
    print('record type: ' + str(record_type))
    print('timestamp: ' + str(timestamp))
    print('user_id:'  + str(user_id)) 
    if record_type in [CREDIT_TYPE, DEBIT_TYPE]:
      dollar_amount = int.from_bytes(file_content[i+13:i+21], byteorder='big') 
      if user_id == MAGIC_USER_ID:
        user_balance += dollar_amount 
    if record_type == CREDIT_TYPE:
      credit_total += dollar_amount
      i += TRANSACTION_RECORD_LENGTH
    elif record_type == DEBIT_TYPE:
      debit_total += dollar_amount
      i += TRANSACTION_RECORD_LENGTH
    elif record_type == AUTOPAY_START_TYPE:
      num_autopays_started += 1
      i += AUTOPAY_RECORD_LENGTH 
    elif record_type == AUTOPAY_END_TYPE:
      num_autopays_ended += 1
      i += AUTOPAY_RECORD_LENGTH
    else:
      print('ERROR: invalid record type ' + str(record_type))
      exit() 
  
  print('Total amount in dollars of debits: ' + debit_total) 
  print('Total amount in dollars of credits: ' + credit_total)
  print('Total number of autopays started: ' + num_autopays_started)
  print('Total number of autopays ended: ' + num_autopays_ended)
  print('Balance of user ID 2456938384156277127: ' + user_balance)

test_file_name = './test_files/txnlog.dat'
read_file(test_file_name)
