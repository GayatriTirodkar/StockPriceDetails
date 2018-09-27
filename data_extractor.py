from bs4 import BeautifulSoup
import requests
import re
import MySQLdb

db = MySQLdb.connect(host="localhost", user="demo", passwd="goodpassword", db="stocks")
cursor = db.cursor()


def execute_crawler():
    all_company_list_url = "https://www.moneycontrol.com/india/stockpricequote/"
    all_company_list_page = requests.get(all_company_list_url)
    all_company_list_page = BeautifulSoup(all_company_list_page.text, "html.parser")
    pagenation_link_list =  all_company_list_page.find('div', attrs={'class':'MT2 PA10 brdb4px alph_pagn'})
    pagenation_link_list = [link for link in pagenation_link_list if link.name == 'a' ]

    for link in pagenation_link_list:
        print "===****Alphabetical Company Scanning for Letter: {}****===".format(link.text)
        alphabetical_page = requests.get("https://www.moneycontrol.com/" + link['href'])
        alphabetical_page = BeautifulSoup(alphabetical_page.text, "html.parser")
        company_name_list = alphabetical_page.find('table', attrs={'class':'pcq_tbl MT10'})
        company_name_rows = company_name_list.find_all('tr')[1:]
        for company_names in company_name_rows:
            final_ar = filter(lambda x: x, alphabetical_page_crawler(company_names))
            sql_insert(final_ar)
            print "=="*20

def alphabetical_page_crawler(company_names):
    all_details_ar = []
    for company in company_names.find_all('td'):
        if len(company.a.text) > 0:
            name = company.text.encode('utf-8').strip()
            company_url = company.a['href'].encode('utf-8').strip()
            try:
                print company_url
                requests.get(company_url)
                all_details_ar.append(get_alphabetical_companies(company_url, name))
            except:
                with open("companies_excluded.txt","a") as appendfile:
                    appendfile.write(company_url+'\n')
                continue
    return all_details_ar

def get_alphabetical_companies(company_url, name):
    print "---Details for Company: {}---".format(name)
    company_details_page = requests.get(company_url)
    company_details_soup = BeautifulSoup(company_details_page.text, 'html.parser') if company_details_page.status_code == 200 else None
    company_details = extract_company_basic_details(company_details_soup) if company_details_soup else None
    if company_details:
        company_details["url"] = company_url.encode('utf-8')
        company_details["name"] = re.sub(r'[^a-zA-Z\s]', "", name)
        company_adv_details = company_details_soup.find_all('div', attrs={'id':'mktdet_1'})
        return extract_company_details(company_adv_details, company_details)
    else:
        print "No records found for: {}".format(name)

def extract_company_basic_details(company_page):
    company_basic_detail = {}
    basic_detail_arr = [basic_detail.text.encode('utf-8') for basic_detail in company_page.find_all('div', attrs={'class':'FL gry10'})]
    if len(basic_detail_arr) > 0:
        basic_detail_arr = map(lambda x: x.strip(), "".join(basic_detail_arr).split('|')[:-2])
        for basic_detail in basic_detail_arr:
            details = basic_detail.split(':')
            company_basic_detail[details[0].lower().strip()] = details[-1].strip()
        return company_basic_detail
    else:
        return
def extract_company_details(company_adv_details, company_details):
    for detail in company_adv_details:
        required_data = [re.sub(r'[^a-zA-Z0-9\.]', "", each.text.encode('utf-8')) for each in detail.find_all('div', attrs={'class':'FR gD_12'})]
        company_details["market_capital"] = 0 if required_data[0] == "" else float(required_data[0])
        company_details['pe_ratio'] = 0 if required_data[1] == "" else float(required_data[1])
        company_details['book_value'] = 0 if required_data[2] == "" else float(required_data[2])
        company_details['div_percent'] = 0 if required_data[3] == "" else float(required_data[3])
        company_details['market_lot'] = 0 if required_data[4] == "" else float(required_data[4])
        company_details['industry_pe_ratio'] = 0 if required_data[5] == "" else float(required_data[5])
        company_details['eps_ttm'] = 0 if required_data[6] == "" else float(required_data[6])
        company_details['pc_value'] = 0 if required_data[7] == "" else float(required_data[7])
        company_details['price_book'] = 0 if required_data[8] == "" else float(required_data[8])
        company_details['div_yield_percent'] = 0 if required_data[9] == "" else float(required_data[9])
        company_details['face_value'] = 0 if required_data[10] == "" else float(required_data[10])
    return company_details

def sql_insert(arr):
    for all_details in arr:
        print "REPLACE INTO stockcompanies VALUES ('"+str(all_details['name'])+"', '"+str(all_details['url'])+"', '"+str(all_details['isin'])+"', '"+str(all_details['sector'])+"', "+str(all_details['market_capital'])+", "+str(all_details['market_lot'])+", "+str(all_details['price_book'])+", "+str(all_details['pc_value'])+", "+str(all_details['pe_ratio'])+", "+str(all_details['div_percent'])+", '"+str(all_details['nse'])+"', '"+str(all_details['bse'])+"', "+str(all_details['industry_pe_ratio'])+", "+str(all_details['div_yield_percent'])+", "+str(all_details['eps_ttm'])+", "+str(all_details['face_value'])+", "+str(all_details['book_value'])+")"
        print "=="*20
        cursor.execute("REPLACE INTO stockcompanies VALUES ('"+str(all_details['name'])+"', '"+str(all_details['url'])+"', '"+str(all_details['isin'])+"', '"+str(all_details['sector'])+"', "+str(all_details['market_capital'])+", "+str(all_details['market_lot'])+", "+str(all_details['price_book'])+", "+str(all_details['pc_value'])+", "+str(all_details['pe_ratio'])+", "+str(all_details['div_percent'])+", '"+str(all_details['nse'])+"', '"+str(all_details['bse'])+"', "+str(all_details['industry_pe_ratio'])+", "+str(all_details['div_yield_percent'])+", "+str(all_details['eps_ttm'])+", "+str(all_details['face_value'])+", "+str(all_details['book_value'])+")")
        db.commit()
        print "Record for company: {} inserted successfully. ".format(all_details["name"])

if __name__ == '__main__':
    print  "Creating stockcompanies table..........."
    cursor.execute("CREATE TABLE IF NOT EXISTS stockcompanies (name VARCHAR(250), url VARCHAR (1024),isin VARCHAR(50) PRIMARY KEY, sector VARCHAR(300), market_capital DECIMAL(20,2),market_lot DECIMAL(20, 2), price_book DECIMAL(20, 2), pc_value DECIMAL(20, 2),pe_ratio DECIMAL(20, 2), div_percent DECIMAL(20, 2), nse VARCHAR(250),bse VARCHAR(250), industry_pe_ratio DECIMAL(20, 2),  div_yield_percent DECIMAL(20, 2),eps_ttm DECIMAL(20, 2), face_value DECIMAL(20,2), book_value DECIMAL(20, 2));")
    print "Table creation successful."
    print "Primary key set successfully. Executing crawler for data extraction..............."
    execute_crawler()
