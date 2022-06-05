import requests
from timeit import default_timer as timer

start = timer()
# ...

# Making a get request
response = requests.get( 'http://www.ucdavis.edu/admissions/undergraduate/transfer/transfer-opportunity-program/participating-collegescampus-life/things-to-do/calendar/colleges-schools-libraries/library'
,verify = False)
  
# print response
#print(response)
  
# print if status code is less than 400
print(response.ok == False)

end = timer()
print(end - start)