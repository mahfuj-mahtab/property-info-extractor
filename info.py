import requests
from bs4 import BeautifulSoup
import pandas as pd


property_link_list=[]
property_type_list=[]
location_list=[]
price_list=[]
img_list=[]
feature_list=[]
description_list=[]
url='https://www.rightmove.co.uk'
main_url1="https://www.rightmove.co.uk/overseas-property-for-sale/USA.html?sortType=2&index="
main_url2="&propertyTypes=&mustHave=&dontShow=&keywords="

r=requests.get('https://www.rightmove.co.uk/overseas-property-for-sale/USA.html?sortType=2&index=0&propertyTypes=&mustHave=&dontShow=&keywords=', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'})

soup=BeautifulSoup(r.content, "html.parser")
find_all_div=soup.find_all('div', {"class":"propertyCard-wrapper"})
# page=soup.find("div", {"class":"pagination-pageSelect"})
page=soup.find("span",{"class":"searchHeader-resultCount"})

p=int(page.text.replace(",",""))


for i in range(0,p+1,24):
    r1=requests.get(main_url1+str(i)+main_url2, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'})
    print(main_url1+str(i)+main_url2)
    print(r1.status_code)
    soup1=BeautifulSoup(r1.content, "html.parser")
    find_all_div=soup1.find_all('div', {"class":"propertyCard-wrapper"})
    for item in find_all_div:
        property_link=item.find("a", {"class":"propertyCard-link"})
        property_link_list.append(property_link['href'])


    for link in property_link_list:
        r2=requests.get(url + link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'})
        soup2=BeautifulSoup(r2.content, "html.parser")
        property_div=soup2.find("div", {"class": "propertydetails"})
        try:
            property_type=property_div.find("h1",{"id":"propertytype"})
            property_type_list.append(property_type.text)
        except:
            feature_list.append("None")
        try:
            location=property_div.find("div", {"id":"addresscontainer"}).find("h2")
            location_list.append(location.text.strip())
        except:
            feature_list.append("None")
        try:
            price=property_div.find("span", {"id":"ospropertyprice"})
            price_list.append(price.text.strip())
        except:
            feature_list.append("None")
        try:
            feature_section=property_div.find("ul",{"class":"keyfeatures"})
            feature_list.append(feature_section.text.replace('\n', '**  '))
        except:
            feature_list.append("None")
        try:
            des=property_div.find_all("div",{"class":"propertyDetailDescription"})
            description_list.append(des[0].text)
        except:
            feature_list.append("None")




    # print(description_list)
    # print(property_link_list)
    # print(property_type_list)
    # print(location_list)
    # print(price_list)
    # print(feature_list)



df=pd.DataFrame({"Property Type":property_type_list,"Property Price": price_list,"Location": location_list, "Top Feature":feature_list,"Description": description_list, "Property link": property_link_list})
df.to_csv("output.csv")