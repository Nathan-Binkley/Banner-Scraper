import requests

URL = 'https://regssb.bannerxe.clemson.edu/StudentRegistrationSsb/ssb/searchResults/searchResults?txt_subjectcoursecombo=CPSC1010&txt_term=202008&pageOffset=0&pageMaxSize=10&sortColumn=subjectDescription&sortDirection=asc&[object%20Object]'

response = requests.get(URL, verify = False)

content = response.content

print(response)
print(response.status_code)
print(content)