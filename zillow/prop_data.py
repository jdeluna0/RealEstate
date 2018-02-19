import requests
import urllib
import csv
from bs4 import BeautifulSoup
import pandas as pd
import sys

data_file = 'cur_for.txt'
getComp_url = 'http://www.zillow.com/webservice/GetComps.htm'
getDeepComp_url = 'http://www.zillow.com/webservice/GetDeepComps.htm'


class zillow_property_info:
    def __init__(self, zwsid='X1-ZWz18ruvvc1ngr_9ej1g'):
        self.zws_id=zwsid

    def send_request(self, url, payload):
        r = requests.post(url,payload)
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup

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
        info_list = []
        for house in data_list:
            in_csz = house[2]+','+'TX'+' '+house[1] 
            citystatezip = urllib.urlencode({'citystatezip':in_csz})
            address = urllib.urlencode({'address':house[0]})
            url = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id={0}&{1}&{2}'.format(self.zws_id,address,citystatezip)
            r = requests.post(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            if soup.code.string != '0':
	        print soup.text
            try:
                info_list.append({'Address':soup.address.string,'CSZ':soup.citystatezip.string,'zpid':soup.zpid.string,'zestimate':'{0:,}'.format(int(soup.zestimate.amount.string))})
            except:
                info_list.append({'Address':house[0],'CSZ':in_csz,'zpid':'NONE','zestimate':'NONE'})
        df = pd.DataFrame(info_list)
        return df

#    def getComps(self, df_data):
#        comps = []
#        for zpid in df_data['zpid']:
#            data = {'zws-id':self.zws_id,'zpid':zpid, 'count':1}
#            soup = self.send_request(getComp_url,data)
#            try:
#                comps.append("{0}; EST: {1:,}".format(soup.properties.comp.address.street.string,int(soup.properties.comp.zestimate.amount.string)))
#            except:
#                comps.append("None Found")
#        df_data['Comparison'] = comps
#        return df_data

    def getDeepComps(self, df_data):
        comps = []
        details = []
        for zpid in df_data['zpid']:
        #    data = {'zws-id':self.zws_id,'zpid':zpid, 'count':1}
	    zpid = urllib.urlencode({'zpid':zpid})
	    count = urllib.urlencode({'count':1})
            url = 'http://www.zillow.com/webservice/GetDeepComps.htm?zws-id={0}&{1}&{2}'.format(self.zws_id,zpid,1)
            #soup = self.send_request(getDeepComp_url,data)
            #soup = self.send_request(getDeepComp_url,data)
	    r = request.post(url)
	    soup = BeautifulSoup(r.content, 'html.parser')
            if soup.code.string != '0':
	        print soup.text
            try:
               comps.append("{0}; EST: {1:,}".format(soup.properties.comp.address.street.string,int(soup.properties.comp.zestimate.amount.string)))
            except:
                comps.append("None Found")
            try:
           	details.append({'Year Built':soup.yearbuilt.string,'SQ FT':soup.finishedsqft.string,'Baths':soup.bathrooms.string,'Beds':soup.bedrooms.string,'Tax Assess':"{0:,}".format(float(soup.taxassessment.string)),'Tax Assess Year':soup.taxassessmentyear.string})
            except:
		e = sys.exc_info()[0]
		print "Error: {0}".format(e)
                details.append({'Year Built':'None','SQ FT':'None','Baths':'None','Beds':'None','Tax Assess':'None','Tax Assess Year':'None'})
        df_data['Comparison'] = comps
        df_data = pd.concat([df_data,pd.DataFrame(details)], axis=1)
        return df_data



p = zillow_property_info()
data_list = p.parse_data_file(data_file)

#df_data = p.getSearch(data_list)
#deets = p.getDeepComps(df_data)
data = p.getDeepComps(p.getSearch(data_list))
