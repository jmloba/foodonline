from datetime import time, datetime, date

# output : [('12:00 am','12:00 am'),('12:00 am','12:30 pm')]

def create_time_slot():
  '''
  for h in range(0,24):
    for m in  (0,30):
      print (f"  result--> {      time(h,m).strftime('%I:%M %p')      } ")
  '''


  t1 =     [ time(h).strftime('%I:%M %p') for h in range(0,24)  ]  
  print(f't1 : {t1}')



  t2 =     [ time(h,m).strftime('%I:%M %p') for h in range(0,24) for m in  (0,30) ]  
  print(f't2 : {t2}')

  # to get the tupple
  result =[ (time(h,m).strftime('%I:%M %p'),time(h,m).strftime('%I:%M %p')) for h in range(0,24) for m in  (0,30) ]  
  print(f'result : {result}')

def today_is ():
  print('jovemn')
  date_today = date.today()

  dt = datetime.now()
  day_of_week = dt.weekday()
  day_no = day_of_week + 1
  print(f'date_today : {date_today}, day of week {day_of_week}, day_no is :{day_no}')

  
def time_at_the_moment():
  time = 1
    
  now = datetime.now()

  current_time = now.strftime("%H:%M:%S")
  
  print(f'---->>> Current Time : {current_time} <<< -----')


# create_time_slot()
# today_is()
time_at_the_moment()
  

