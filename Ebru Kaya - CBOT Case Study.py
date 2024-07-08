#!/usr/bin/env python
# coding: utf-8

# In[1]:


##Kütüphane tanımlamaları yapılmıştır.

from bs4 import BeautifulSoup
from tabulate import tabulate
import requests
import pandas as pd
pd.set_option('display.max_rows', None)


# In[2]:


##"https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue" adresinde yer alan tablodaki 
##bilgiler çekilmiş ve kullanıma hazır olacak şekilde tabloya dönüştürülmüştür.


url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html')

table = soup.find_all('table')[1]
world_titles = table.find_all('th')
world_table_titles = [title.text.strip() for title in world_titles]

df = pd.DataFrame(columns = world_table_titles)

column_data = table.find_all('tr')

for row in column_data[1:]:
    row_data = row.find_all('td')
    individual_row_data = [data.text.strip() for data in row_data]
    
    length = len(df)
    df.loc[length] = individual_row_data
    

    
df['Revenue (USD millions)'] = df['Revenue (USD millions)'].astype(str).apply(lambda x: x.replace(',',''))
df['Revenue (USD millions)'] = df['Revenue (USD millions)'].astype(int)    
    
df['Employees'] = df['Employees'].astype(str).apply(lambda x: x.replace(',',''))
df['Employees'] = df['Employees'].astype(str).apply(lambda x: x.replace('[2]',''))
df['Employees'] = df['Employees'].astype(int)    
    
df['Revenue growth'] = df['Revenue growth'].astype(str).apply(lambda x: x.replace('%',''))
df['Revenue growth'] = df['Revenue growth'].astype(float)

df.loc[26,'Revenue growth'] = -df.loc[26,'Revenue growth']
df.loc[29,'Revenue growth'] = -df.loc[29,'Revenue growth']
df.loc[30,'Revenue growth'] = -df.loc[30,'Revenue growth']
df.loc[33,'Revenue growth'] = -df.loc[33,'Revenue growth']
df.loc[54,'Revenue growth'] = -df.loc[54,'Revenue growth']
df.loc[61,'Revenue growth'] = -df.loc[61,'Revenue growth']
df.loc[63,'Revenue growth'] = -df.loc[63,'Revenue growth']
df.loc[64,'Revenue growth'] = -df.loc[64,'Revenue growth']
df.loc[66,'Revenue growth'] = -df.loc[66,'Revenue growth']
df.loc[68,'Revenue growth'] = -df.loc[68,'Revenue growth']
df.loc[85,'Revenue growth'] = -df.loc[85,'Revenue growth']
df.loc[95,'Revenue growth'] = -df.loc[95,'Revenue growth']
df.loc[96,'Revenue growth'] = -df.loc[96,'Revenue growth']


# In[3]:


##Chatbot modeli oluşturularak belli başlı sorulara hem standart hem de interaktif cevaplar verecek şekilde kurgulanmıştır.


print("CBOT:\nMerhaba ben CBOT. \n\n2023 yılı Amerika Birleşik Devletleri'nde yer alan kazanç bazındaki en büyük şirketler konusunda uzmanlaşmış bir chatbotum. \n\nSize nasıl yardımcı olabilirim? \n\n 1-Tüm şirketleri görmek istiyorum. \n 2-Firma ismi ile arama yapmak istiyorum. \n 3-Sektörel bazda arama yapmak istiyorum. \n 4-Bölgesel bazda arama yapmak itiyorum. \n 5-Detaylı arama yapmak istiyorum. \n\nSorunuza ait numarayı giriniz.")

while True:
    user_input1 = input("\nSiz: ")
    
    if user_input1 == "1":
        print("\nCBOT:\n")
        print(df)
        break
    
    if user_input1 == "2":
        print("\nCBOT: Hangi firmanın bilgilerini görmek istersiniz? (Örn: Amazon, Apple, Microsoft vb.)")
        user_input2 = input("\nSiz: ")
        answer = df[df['Name'] == user_input2]
        print("\nCBOT:\n")
        print(answer)
        break
            
    if user_input1 == "3":
        print("\nCBOT: Hangi sektöre ait firmaları görmek istersiniz? (Örn: Technology, Retail, Financials vb.)")
        user_input2 = input("\nSiz: ")
        answer = df[df['Industry'] == user_input2]
        print("\nCBOT:\n")
        print(answer)
        break
        
    if user_input1 == "4":
        print("\nCBOT: Hangi bölgedeki firmaları görmek istersiniz? (Örn: New York, Texas, Washington vb.)")
        user_input2 = input("\nSiz: ")
        answer = df[df['Headquarters'].str.contains(user_input2, case=False, na=False)]
        print("\nCBOT:\n")
        print(answer)
        break
        
    if user_input1 == "5":
        print("\nCBOT: \n 1-En yüksek ve en düşük gelire sahip firmalar hangileridir?. \n 2-En fazla ve en az çalışana sahip olan firmalar hangileridir? \n 3-En yüksek gelir artışı ve en yüksek gelir kaybına sahip olan firmalar hangileridir? \n 4-Geliri artan firmalar hangileridir? \n 5-Geliri azalan firmalar hangileridir? \n 6-Özel filtreleme yapmak istiyorum.")
        user_input2 = input("\nSiz: ")
        
        if user_input2 == "1":
            answer = df.loc[df['Revenue (USD millions)'].idxmax()]
            print("\nCBOT:\nEn yüksek gelire sahip firma\n") 
            print(answer)
            answer2 = df.loc[df['Revenue (USD millions)'].idxmin()]
            print("\nCBOT:\nEn düşük gelire sahip firma\n") 
            print(answer2)
            break
            
        if user_input2 == "2":
            answer = df.loc[df['Employees'].idxmax()]
            print("\nCBOT:\nEn fazla çalışan sayısına sahip firma\n") 
            print(answer)
            answer2 = df.loc[df['Employees'].idxmin()]
            print("\nCBOT:\nEn az çalışan sayısına sahip firma\n") 
            print(answer2)
            break
            
        if user_input2 == "3":
            answer = df.loc[df['Revenue growth'].idxmax()]
            print("\nCBOT:\nEn yüksek gelir artışına sahip firma\n") 
            print(answer)
            answer2 = df.loc[df['Revenue growth'].idxmin()]
            print("\nCBOT:\nEn yüksek gelir kaybına sahip firma\n") 
            print(answer2)
            break
            
        if user_input2 == "4":
            answer = df[(df['Revenue growth'] > 0)]
            print("\nCBOT:\nGeliri artan firmalar\n") 
            print(answer)
            break
            
        if user_input2 == "5":
            answer = df[(df['Revenue growth'] < 0)]
            print("\nCBOT:\nGeliri azalan firmalar\n") 
            print(answer)
            break
            
        if user_input2 == "6":
            print("\nCBOT: \n 1-Geliri belirli bir rakamdan fazla olan firmalar hangileridir? \n 2-Geliri belirli bir rakamdan az olan firmalar hangileridir? \n 3-Çalışan sayısı belirli bir rakamdan fazla olan firmalar hangileridir? \n 4-Çalışan sayısı belirli bir rakamdan az olan firmalar hangileridir? \n 5-Gelir artışı belirli bir rakamdan fazla olan firmalar hangileridir? \n 6-Gelir artışı belirli bir rakamdan az olan firmalar hangileridir? \n 7-Müşteri temsilcisine bağlanmak istiyorum.")
            user_input3 = input("\nSiz: ")
            
            if user_input3 == "1":
                print("\nCBOT: Rakam giriniz. (Milyar USD cinsinden)")
                user_input4 = int(input("\nSiz: "))
                for i in range(100):
                    df.loc[i,'Revenue (USD millions)'] = df.loc[i,'Revenue (USD millions)']/1000
                answer = df[(df['Revenue (USD millions)'] > user_input4)]
                print("\nCBOT:\n") 
                print(answer)
                for i in range(100):
                    df.loc[i,'Revenue (USD millions)'] = df.loc[i,'Revenue (USD millions)']*1000
                break
                
            if user_input3 == "2":
                print("\nCBOT: Rakam giriniz. (Milyar USD cinsinden)")
                user_input4 = int(input("\nSiz: "))
                for i in range(100):
                    df.loc[i,'Revenue (USD millions)'] = df.loc[i,'Revenue (USD millions)']/1000
                answer = df[(df['Revenue (USD millions)'] < user_input4)]
                print("\nCBOT:\n") 
                print(answer)
                for i in range(100):
                    df.loc[i,'Revenue (USD millions)'] = df.loc[i,'Revenue (USD millions)']*1000
                break
                
            if user_input3 == "3":
                print("\nCBOT: Rakam giriniz.")
                user_input4 = int(input("\nSiz: "))
                answer = df[(df['Employees'] > user_input4)]
                print("\nCBOT:\n") 
                print(answer)
                break
                
            if user_input3 == "4":
                print("\nCBOT: Rakam giriniz.")
                user_input4 = int(input("\nSiz: "))
                answer = df[(df['Employees'] < user_input4)]
                print("\nCBOT:\n") 
                print(answer)
                break
                
            if user_input3 == "5":
                print("\nCBOT: Rakam giriniz. (% cinsinden)")
                user_input4 = int(input("\nSiz: "))
                answer = df[(df['Revenue growth'] > user_input4)]
                print("\nCBOT:\n") 
                print(answer)
                break
                             
            if user_input3 == "6":
                print("\nCBOT: Rakam giriniz. (% cinsinden)")
                user_input4 = int(input("\nSiz: "))
                user_input4 = -user_input4
                answer = df[(df['Revenue growth'] < user_input4)]
                print("\nCBOT:\n") 
                print(answer)
                break
                
            if user_input3 == "7":
                print("\nCBOT: Destek olamadığım için üzgünüm, sizi müşteri temsilcinize aktarıyorum.")
                break


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




