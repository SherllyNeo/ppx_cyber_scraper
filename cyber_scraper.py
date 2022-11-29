import requests
import random
import time
import pandas as pd
import json
import string

print("cyber scraper start...")
all_three_letters = list()
letters = list(string.ascii_lowercase)
for i in letters:
    for j in letters:
        for k in letters:
            s = i + j + k
            all_three_letters.append(s)

print("generated all letter triples, starting scraper...")
random.shuffle(all_three_letters)

class Company:
    def __init__(self,ABCertificateReference,AccreditationBody,CertID,CertificateLevel,CertificationBody,CertificationDate,CompanyAddress,CompanyName,Sector,Scope):
        self.ABCertificateReference = ABCertificateReference
        self.AccreditationBody = AccreditationBody
        self.CertID = CertID
        self.CertificateLevel = CertificateLevel
        self.CertificationBody = CertificationBody
        self.CertificationDate =  CertificationDate
        self.CompanyAddress = CompanyAddress
        self.CompanyName = CompanyName
        self.Sector = Sector
        self.Scope = Scope

class Cyber_Scraper:
    def __init__(self,search_term):
        self.limit = 50
        self.url = f"https://db.iasme.co.uk/certSummarySearch.php?query={search_term}&pageNum=1&limit={self.limit}"
        self.term = search_term
    def request_search(self):
        frame = pd.DataFrame(columns=['ABCertificateReference','AccreditationBody','CertID','CertificateLevel','CertificationBody','CertificationDate','CompanyName','CompanyAddress','Sector','Scope'])
        result = requests.get(self.url).json()
        print(result)
        try:
            response = result['result']
        except Exception as e:
            print(f"{self.term} failed because {e}")
            return None
        for company_json in response:
            try:
                list_to_appened = [company_json["ABCertificateReference"],company_json["AccreditationBody"],company_json["CertID"],company_json["CertificateLevel"],company_json["CertificationBody"],company_json["CertificationDate"],company_json["CompanyName"],company_json["CompanyAddress"],company_json["Sector"],company_json["Scope"]]
                frame.loc[len(frame)] = list_to_appened
            except:
                pass
        return frame

def grab_csv():
    try:
        csv = pd.read_csv("final_companies.csv")
        return csv
    except:
        csv = pd.DataFrame(columns=['ABCertificateReference','AccreditationBody','CertID','CertificateLevel','CertificationBody','CertificationDate','CompanyName','CompanyAddress','Sector','Scope'])
        return csv





def entrypoint():
    list_of_all_companies = list()
    for term in all_three_letters:
        csv = grab_csv()
        time.sleep(10)
        print(f"scraping {term}")
        scraper = Cyber_Scraper(term).request_search()
        list_of_all_companies.append(scraper)
        df_temp = pd.concat([csv,scraper])
        print(df_temp)
        df_temp = df_temp[['ABCertificateReference','AccreditationBody','CertID','CertificateLevel','CertificationBody','CertificationDate','CompanyName','CompanyAddress','Sector','Scope']]
        df_temp.to_csv("final_companies.csv")
    df = pd.concat(list_of_all_companies)

    df = df[['ABCertificateReference','AccreditationBody','CertID','CertificateLevel','CertificationBody','CertificationDate','CompanyName','CompanyAddress','Sector','Scope']]

    print(df)
    df.to_csv("final_companies.csv")


entrypoint()



def test():
    search_term = "AIM"
    limit = 50
    url = f"https://db.iasme.co.uk/certSummarySearch.php?query={search_term}&pageNum=1&limit={limit}"
    response = requests.get(url).json()['result']
    print(response)
