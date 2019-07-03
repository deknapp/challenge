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
HEADER_LENGTH = 9

def read_file(file_name):
  handle = open(file_name, 'rb')
  file_content = handle.read() 
  version = file_content[4]
  num_records = int.from_bytes(file_content[5:9], byteorder='big') 
  
  debit_total = 0
  credit_total = 0
  num_autopays_started = 0
  num_autopays_ended = 0 
  record_start = HEADER_LENGTH
  user_balance = 0 
  for record in range(num_records): 
    record_type = file_content[record_start]
    timestamp = int.from_bytes(file_content[record_start+1:record_start+5], byteorder='big')
    user_id = int.from_bytes(file_content[record_start+5:record_start+13], byteorder='big')    
    dollar_amount = 0 
    if record == 0:
      print('record type: ' + str(record_type))
      print('timestamp: ' + str(timestamp))
      print('user_id: '  + str(user_id)) 
    if record_type in [CREDIT_TYPE, DEBIT_TYPE]:
      dollar_amount = struct.unpack('>d', file_content[record_start+13:record_start+21])[0] 
      if record == 0:
        print('dollar_amount: ' + str(dollar_amount))
      if user_id == MAGIC_USER_ID:
        user_balance += dollar_amount 
    if record_type == CREDIT_TYPE:
      credit_total += dollar_amount
      record_start += TRANSACTION_RECORD_LENGTH
    elif record_type == DEBIT_TYPE:
      debit_total += dollar_amount
      record_start += TRANSACTION_RECORD_LENGTH
    elif record_type == AUTOPAY_START_TYPE:
      num_autopays_started += 1
      record_start += AUTOPAY_RECORD_LENGTH 
    elif record_type == AUTOPAY_END_TYPE:
      num_autopays_ended += 1
      record_start += AUTOPAY_RECORD_LENGTH
    else:
      print('ERROR: invalid record type ' + str(record_type))
      exit() 
  
  print('Total amount in dollars of debits: ' + str(debit_total)) 
  print('Total amount in dollars of credits: ' + str(credit_total))
  print('Total number of autopays started: ' + str(num_autopays_started))
  print('Total number of autopays ended: ' + str(num_autopays_ended))
  print('Balance of user ID 2456938384156277127: ' + str(user_balance))

test_file_name = './test_files/txnlog.dat'
read_file(test_file_name)
