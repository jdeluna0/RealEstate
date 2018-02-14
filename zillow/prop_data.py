import requests
import urllib
import csv
from bs4 import BeautifulSoup

data_file = 'cur_for.txt'

class zillow_property_info:
    def __init__(self, zwsid='X1-ZWz18ruvvc1ngr_9ej1g'):
        self.zws_id=zwsid

    def parse_data_file(self, data_file):
        try:
            with open(data_file) as csvfile:
                reader = csv.reader(csvfile) 
                data = list(reader)
                return data
        except:
            print
            print 'No data file found.'
            sys.exit(1)

    def getSearch(self, data_list): 
        info_dict = {}
        for house in data_list:
            in_csz = house[2]+','+'TX'+' '+house[1] 
            citystatezip = urllib.urlencode({'citystatezip':in_csz})
            address = urllib.urlencode({'address':house[0]})
            url = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id={0}&{1}&{2}'.format(self.zws_id,address,citystatezip)
            # print url
            r = requests.post(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            try:
                info_dict[soup.zpid.string] = [soup.address.string,soup.citystatezip.string,soup.zpid.string,soup.zestimate.amount.string]
            except:
                info_dict.[soup.zpid.string] = [house[0],in_csz,'NONE','NONE']
                continue
              #  for i in range(0,4):
              #      if entry != None:
              #          print "{}\t".format(entry[i]),
              #      else:
              #          print "NONE"
            #break
        return info_list

   # def getEstimate():


p = zillow_property_info()
data_list = p.parse_data_file(data_file)
zpid_and_estimates = p.getSearch(data_list)
things = p.getEstimate(zpid_and_estimates)
