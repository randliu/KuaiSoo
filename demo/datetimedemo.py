import datetime
delta=datetime.timedelta(seconds=120)
now = datetime.datetime.now()
print now 
expire_date = now + delta
print expire_date
print expire_date > datetime.datetime.now()
print datetime.datetime.time()
 