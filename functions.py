import urllib.request as urllib2
from bs4 import BeautifulSoup
import datetime

coronaData_ = {}

def coronaData():
    page = urllib2.urlopen("https://www.mohfw.gov.in/")
    soup = BeautifulSoup(page, 'html.parser')
    div = soup.findAll('div',attrs={'class':'table-responsive'})[0]
    table = div.find_all('tbody')[0]
    rows = table.find_all('tr')
    data = {}
    for tr in rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        if(len(row)==6):
            data[row[1].lower()] = {
                "tccin": row[2].rstrip().lstrip(),
                "tccfn": row[3].rstrip().lstrip(),
                "cured": row[4].rstrip().lstrip(),
                "death": row[5].rstrip().lstrip(),
            }
        else:
            data["india"] = {
                "tccin": row[1].rstrip().lstrip(),
                "tccfn": row[2].rstrip().lstrip(),
                "cured": row[3].rstrip().lstrip(),
                "death": row[4].rstrip().lstrip(),
            }
    data["updated"] = datetime.datetime.now().strftime("%d %B, %Y - %H:%M:%S")
    global coronaData_
    coronaData_ = data
    print(coronaData_)

def getStateWiseCorona(state):
    print(coronaData_, type(coronaData_))
    answer = "Total Confirmed Case (Indian National) : {}<br>Total Confirmed Case (Foreign National) : {}<br>Cured : {}<br>Death : {}<br>Last Updated : {}".format(coronaData_[state]["tccin"], coronaData_[state]["tccfn"], coronaData_[state]["cured"], coronaData_[state]["death"], coronaData_["updated"])
    return answer

coronaData()