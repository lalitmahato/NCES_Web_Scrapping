# importing library
import requests
from bs4 import BeautifulSoup
import json

university_data = []
error_to_phase = []
error_to_phase2 = []

def getData(UniId, uCount):
    url = "https://nces.ed.gov/ipeds/datacenter/institutionprofile.aspx?unitId=" + str(UniId)
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')

    
    University_Data = soup.find_all('div', style="padding-top:7px; padding-bottom:7px;") # all the data related to university
    Information_Hadings = soup.find_all('div', style="float:left; padding-left:5px; padding-top:3px;") # phase university data
    Main_Headers = []  # list to store university information headers
    University_Information = {}
    for header in Information_Hadings:
        title_header = header.get_text(separator=' ').split()
        title_header = [x.capitalize() for x in title_header] # capitalizing all the first letters
        title_header = "_".join(title_header)
        Main_Headers.append(title_header) # adding to the Main_Headers list 
    # print(Main_Headers)
    # print(len(University_Data))
    count = 0
    for uni_data in University_Data:
        # print(uni_data)
        # print("count: ",count)
        content = uni_data.find_all('div', style="padding-bottom:30px;display:none;")
        Table_Title = []
        Table_Sub_Title = []
        for con in content:
            Table_Title = [x.get_text(separator=' ') for x in con.find_all('div', style="text-align:left; vertical-align:middle;font-size:12px;font-weight:bold;font-family:verdana, Arial;color:#4578ad;padding-top:17px; padding-bottom:14px;")]
            Table_Sub_Title = [x.get_text(separator=' ') for x in con.find_all('div', style="text-align:left; vertical-align:middle;font-size:12px;font-weight:bold;font-family:verdana, Arial;color:#4578ad;padding-top:30px; padding-bottom:14px;")]
            Table_Data = {} # palce to store all table data
            tables = con.find_all('table')
            # print("Number of Table: ", len(tables))
            table_count = 0
            for tab in tables:
                table_name = ""
                table_headings = [x for x in tab.find_all('tr', class_="idc_ip_header_tr")]
                main_table_headings = []
                for t_h in table_headings:
                    main_table_headings = [x.get_text(separator=' ') for x in t_h.find_all('td')]
                main_table_headings = ["_".join(x.split()) for x in main_table_headings]
                # print(main_table_headings)
                main_table_sub_headings = [x.get_text(separator=' ') for x in tab.find_all('td', class_="idc_ip_subheader_td")]
                tab_content = [x for x in tab.find_all('tr', class_="idc_ip_tr")]
                Table_Content = {}
                for tab_con in tab_content:
                    table_content = [x.get_text(separator=' ') for x in tab_con.find_all('td')]
                    topic = [x.strip().capitalize() for x in table_content[0].split()]

                    if Main_Headers[count] == "Net_Price":
                        topic = "".join(topic)
                    else:
                        topic = "_".join(topic)

                    if len(main_table_headings) == 0:
                        Table_Content[topic] = table_content[1].strip()
                        if Main_Headers[count] == "Student_Charges":
                            table_name = "Cost"
                            # print("table_name: ", table_name)
                        elif Main_Headers[count] == "Finance":
                            if table_count == 0:
                                table_name = "Core_Revenues_Per_FTE_Enrollment"
                            elif table_count == 1:
                                table_name = "Core_Expenses_Per_FTE_Enrollment"
                    else:
                        table_data = {}
                        if len(main_table_sub_headings) == 0:
                            for heading in range(len(main_table_headings)-1):    
                                try:
                                    table_data[main_table_headings[heading+1]] = table_content[heading+1]
                                except:
                                    table_data[main_table_headings[heading+1]] = ""
                            Table_Content[topic] = table_data
                            if Main_Headers[count] == "Completions":
                                # print(table_count)
                                if table_count == 0:
                                    table_name = "Total"
                                elif table_count == 1:
                                    table_name = "Men"
                                elif table_count == 2:
                                    table_name = "Women"
                                else:
                                    table_name = main_table_headings[0]
                                # print("table_name: ", table_name)
                            elif Main_Headers[count] == "Human_Resources":
                                if table_count == 1:
                                    table_name = "Number_Of_Full-Time_Staff"
                                else:
                                    table_name = main_table_headings[0]
                                    # print("table_name: ", table_name)
                            else:
                                if main_table_headings[0] != "":
                                    table_name = main_table_headings[0]
                                    # print("table_name: ", table_name)
                        else:
                            table_data[main_table_headings[1]] = table_content[1]
                            table_data[main_table_headings[2]] = table_content[2]
                            table_data[main_table_headings[3]] = {'Full_Time': table_content[3],'Part_Time':table_content[4]}
                            Table_Content[topic] = table_data
                            table_name = "Applications"
                            # print("table_name: ", table_name)
                
                # To put the informative table attributes
                if len(tables) == 1:
                    if table_name == "" :
                        table_name = Main_Headers[count]
                        # print("table_name: ", table_name)

                Table_Data[table_name] = Table_Content
                # Table_Data[] = Table_Content     
                # print(main_table_headings)
                # print(main_table_sub_headings)
                print(Table_Content)
                # print("\n")        
            # print(Table_Title)
            # print(len(Table_Sub_Title), Table_Sub_Title)
                table_count = table_count + 1
                
            # print(Table_Data)
            University_Information[Main_Headers[count]] = Table_Data
        # print(University_Information)
        # print(University_Information)
        # University_Information[str(uCount)] = University_Information
        # print("\n\n\n\n\n\n")
        count = count + 1
    # print(University_Information)
    university_data.append({uCount: University_Information})
    # print("\n\n\n\n\n\n")

# # loading json file
# lodeJson = open('unitId.json', "r")
# uId_data = json.load(lodeJson)
# total_uid = len(uId_data)
# scrap_data_count = 0
# for i in uId_data:
#     # print(i['UnitID']) # print university ID
#     print("Total University Count: ", total_uid)
#     perc = scrap_data_count/total_uid * 100
#     if perc < 1:
#         print("*")
#     # print("Completed: {} %".format(perc))
#     for i in range(int(perc)):
#         print("*")
#     print("Completed: {} %".format(perc))
#     print("Data Scraped: ", scrap_data_count)
#     try:
#         getData(i['UnitID'],scrap_data_count+1)
#         scrap_data_count = scrap_data_count + 1
#     except:
#         error_to_phase.append(i['UnitID'])
#     # # clear the screen
#     # clear = lambda: os.system('cls')
#     # clear()
#     print(university_data)

# for j in error_to_phase:
#     try:
#         getData(j,scrap_data_count+1)
#         scrap_data_count = scrap_data_count + 1
#     except:
#         error_to_phase2.append(j)
# print("Unable to phase {} university data".format(len(error_to_phase2)))

# getData(166027, 1)
# # print("********************************************************************")
# getData(180203, 2)
getData(166027, 1)
# getData(437608, 2)
print(university_data)

# To export data in json file
with open("scrapped_university_details1.json", "w") as jsonwrite:
    json.dump(university_data, jsonwrite, indent = 4)
