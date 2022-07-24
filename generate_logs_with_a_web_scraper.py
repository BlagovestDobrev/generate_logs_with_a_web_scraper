import datetime
import random
import requests
from bs4 import BeautifulSoup
from nltk import tokenize
from sys import getsizeof
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

""" 
Python 3.8
The code below will download the data in the paragraphs from the URL written below.
Then will use the text to fill and generate a fictuned log file for test purpose with 10000 lines(each one 500 bytes size).
Then will analyze the log file and display statistics based on how many times same status from the log appres for a minute.
Then will count and order how many times a word appear in the data field in the log file. It will display in the console the 1o words with the mosts counts. 
"""

my_data = []
url = 'https://en.wikipedia.org/wiki/Amazon_S3'

page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")


results = soup.find(id="mw-content-text")
final_res = results.find_all("p")
row_to_generate = 10000
current_date =  datetime.datetime(2013, 1, 1, 9)
end_time = datetime.datetime(2013, 1, 1, 11, 59, 59)
step_of_time = (end_time - current_date) / row_to_generate
current_time = current_date
status = ["OK", "TEMP", "PERM"]
data = "TEST,TEST,TEST"
comment = "X"



for i in final_res:
    for l in tokenize.sent_tokenize(i.text.strip()):
        my_data.append(l)



with open("LOG.txt", "w") as text_file:
    for i in range(row_to_generate):
        current_time += step_of_time
        pid = random.randrange(3000, 5000)
        current_status = random.choice(status)
        data = random.choice(my_data)
        current_row = current_date.strftime('%Y%m%d') + "|" + current_time.strftime('%H:%M:%S') + "|" + str(pid) + "|" + current_status + "|" + data
        if getsizeof(current_row) > 500:
            while getsizeof(current_row) > 500:
                data = random.choice(my_data)
                current_row = current_date.strftime('%Y-%m-%d') + "|" + current_time.strftime('%H:%M:%S') + "|" + str(pid) + "|" + current_status + "|" + data
        while getsizeof(current_row) <= 500:

            temp_row = ""
            if my_data.index(data)+1 < len(my_data):
                temp_row = current_row + my_data[my_data.index(data)+1]

                if getsizeof(temp_row) < 500:
                    current_row += my_data[my_data.index(data)+1]
                    data = my_data[my_data.index(data)+1]
                else:
                    break
            else:
                break

        current_row += "|"
        while getsizeof(current_row) <= 500:
            if getsizeof(current_row + comment) <= 500:
                current_row += comment
            else:
                break

        text_file.write("{0}\n".format(current_row))

state_data_by_time = []

with open("LOG.txt", "r") as text_file:
    for l in text_file:
        current_row_array=l.split("|")
        state_data_by_time.append([current_row_array[1],current_row_array[3]])

data_test={}
prev_minute = "59"
bar_time = ""
PERM_v = 0
TEMP_v = 0
OK_v = 0

for bar in state_data_by_time:
    bar_time = bar[0]
    minute = bar[0].split(":")[1]

    if minute == prev_minute:
        if bar[1] == "PERM" :
            PERM_v+=1
        if bar[1] == "TEMP":
            TEMP_v+=1
        if bar[1] == "OK":
            OK_v+=1
    if minute != prev_minute:
        prev_minute = minute
        new_min_entry = {bar_time : {"PERM":PERM_v,"TEMP":TEMP_v,"OK":OK_v }}
        data_test.update(new_min_entry)
        PERM_v = 0
        TEMP_v = 0
        OK_v = 0

        if bar[1] == "PERM" :
            PERM_v+=1
        if bar[1] == "TEMP":
            TEMP_v+=1
        if bar[1] == "OK":
            OK_v+=1



pd.DataFrame(data_test.values(),index=data_test.keys()).plot.bar()
plt.xlabel('Time')
plt.ylabel('Number')
plt.savefig('results.png')

plt.show()


log_data = ""

with open("LOG.txt", "r") as text_file:
    for l in text_file:
        current_row_array=l.split("|")
        log_data+=current_row_array[4]

tokenizer_data = tokenize.RegexpTokenizer(r'\w+')

words = tokenizer_data.tokenize(log_data)
counts = Counter(words)

most_popular_word = dict(reversed(sorted(counts.items(), key=lambda item: item[1])))

for k in list(most_popular_word)[:10]:
    print(k," - ", most_popular_word[k])
