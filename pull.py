import requests, json

URL = 'https://regssb.bannerxe.clemson.edu/StudentRegistrationSsb/ssb/searchResults/searchResults?txt_subjectcoursecombo=CPSC1010&txt_term=202001&pageOffset=0&pageMaxSize=10&sortColumn=subjectDescription&sortDirection=asc&[object%20Object]'

s = requests.session()

response = s.get(URL, verify = False)

content = response.content
print(response.json())
