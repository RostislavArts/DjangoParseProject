from bs4 import BeautifulSoup
import os
import requests
from selenium import webdriver
import psycopg2
import time

card_name = []
images_url = []
credit_values = []
prices_values = []
product_id = []
videochipset = []
spec_1 = [] 
spec_2 = []
spec_3 = []
spec_4 = []
spec_5 = []
spec_6 = []


os.environ['PATH'] += r"C:/SeleniumDrivers"
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

def parse_names():
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get("https://www.citilink.ru/catalog/videokarty/?sorting=price_asc&view_type=list")
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, features='lxml')

    # searching for names of videocards
    product_names = soup.find_all('div', class_='app-catalog-1tp0ino')

    # adding names to name list
    for name in product_names:
        card_name.append(name.text)

    # this is for debugging purpouses:
    #
    # for card in card_name:
    #     print(card)

    return card_name

def parse_images():

    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get("https://www.citilink.ru/catalog/videokarty/?sorting=price_asc&view_type=list")
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, features='lxml')

    # searching image urls
    product_images = soup.find_all('img', class_='is-selected')

    # adding urls to url list
    for image in product_images:
        images_url.append(image['src'])

    # this is for debugging purpouses:
    #
    # for image in images_url:
    #     print(image)
    
    # downloading images
    for url in images_url:
        response = requests.get(url)
        file_name = url.split('/')[-1]
        with open(f'C:/МИФИ/2 семестр/Алгоритмы и структуры данных/DjangoProject/images/{file_name}', 'wb') as file:
            file.write(response.content)
    
    return images_url

def get_image_by_name(file_name):
    with open(f'C:/МИФИ/2 семестр/Алгоритмы и структуры данных/ParseProject/images/{file_name}', 'rb') as file:
        return file

def parse_credit_values():
    driver.maximize_window()
    driver.implicitly_wait(10)
    data="https://www.citilink.ru/catalog/videokarty/?sorting=price_asc&view_type=list"
    driver.get(data)
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, features='lxml')
    time.sleep(3)

    product_names1 = soup.find_all(class_='app-catalog-9gnskf')

    count = 0
    for i in product_names1:
        if count == 48:
            break
        j = i.get('href')
        driver.get('https://www.citilink.ru/' + str(j) + '/')
        time.sleep(3)
        page_text = driver.page_source
        soup1 = BeautifulSoup(page_text, features='lxml')
        credit = soup1.find('span', class_='app-catalog-1wvrfhj')

        if credit is not None:
            credit_values.append(credit.text)
        else:
            credit_values.append('None')
        count += 1
    
    return credit_values

def parce_prices():
    driver.maximize_window()
    driver.implicitly_wait(10)
    time.sleep(3)
    driver.get("https://www.citilink.ru/catalog/videokarty/?sorting=price_asc&view_type=list")
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, features='lxml')

    product_prices = soup.find_all('div', class_='app-catalog-1ret8x8')

    for price in product_prices:
        prices_values.append(price.text)
    
    for price in prices_values:
        print(price)
    
    return prices_values

def parce_id():
    driver.maximize_window()
    driver.implicitly_wait(10)
    time.sleep(3)
    driver.get("https://www.citilink.ru/catalog/videokarty/?sorting=price_asc&view_type=list")
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, features='lxml')

    all_id = soup.find_all('span', class_='app-catalog-17g0ixa')

    for id in all_id:
        product_id.append(id.text)
    
    return product_id

def parce_spec():
    driver.maximize_window()
    driver.implicitly_wait(10)
    time.sleep(3)
    driver.get("https://www.citilink.ru/catalog/videokarty/?sorting=price_asc&view_type=list")
    html_text = driver.page_source
    soup = BeautifulSoup(html_text, features='lxml')

    all_specs = soup.find_all('li', class_='app-catalog-12y5psc')

    for spec in all_specs:
        if "Видеочипсет" in spec.text:
            spec_1.append(spec.text.replace("Видеочипсет\xa0", ""))
        elif "Память" in spec.text:
            spec_2.append(spec.text.replace("Память\xa0", ""))
        elif "Интерфейс" in spec.text:
            spec_3.append(spec.text.replace("Интерфейс\xa0", ""))
        elif "Разъемы" in spec.text:
            spec_4.append(spec.text.replace("Разъемы\xa0", ""))
        elif "Питание" in spec.text:
            spec_5.append(spec.text.replace("Питание\xa0", ""))
        elif "Охлаждение" in spec.text:
            spec_6.append(spec.text.replace("Охлаждение\xa0", ""))
        elif "Особенности" in spec.text:
            continue
    
    return spec_1, spec_2, spec_3, spec_4, spec_5, spec_6

def send_to_db():
    conn = psycopg2.connect(
        dbname="citilink_videocards",
        user="postgres",
        password="YOUR_PASSWORD",
        host="localhost"
    )

    cur = conn.cursor()

    i = 1

    for image in images_url:
        card = card_name.pop(0)
        short_image = image.split('/')[-1]
        cur.execute(f"INSERT INTO public.videocards(id, name, image_url) VALUES (%s, %s, %s);", (i, card, short_image))
        conn.commit()
        i += 1

    cur.close()
    conn.close()

def send_credit_to_db():
    conn = psycopg2.connect(
        dbname="citilink_videocards",
        user="postgres",
        password="YOUR_PASSWORD",
        host="localhost"
    )

    cur = conn.cursor()

    i = 1

    for credit in credit_values:
        cur.execute(f"UPDATE videocards SET credit_value=%s WHERE id=%s;", (credit, i))
        conn.commit()
        i += 1
    
    cur.close()
    conn.close()

def send_prices_to_db():
    conn = psycopg2.connect(
        dbname="citilink_videocards",
        user="postgres",
        password="YOUR_PASSWORD",
        host="localhost"
    )

    cur = conn.cursor()

    i = 1

    for price in prices_values:
        cur.execute(f"UPDATE videocards SET price=%s WHERE id=%s;", (price, i))
        conn.commit()
        i += 1
    
    cur.close()
    conn.close()

def send_id_to_db():
    conn = psycopg2.connect(
        dbname="citilink_videocards",
        user="postgres",
        password="YOUR_PASSWORD",
        host="localhost"
    )

    cur = conn.cursor()

    i = 1

    for id in product_id:
        cur.execute(f"UPDATE videocards SET product_id=%s WHERE id=%s;", (id, i))
        conn.commit()
        i += 1
    
    cur.close()
    conn.close()

def send_spec_to_db():
    conn = psycopg2.connect(
        dbname="citilink_videocards",
        user="postgres",
        password="YOUR_PASSWORD",
        host="localhost"
    )

    cur = conn.cursor()

    i = 1

    for spec in spec_1:
        cur.execute(f"UPDATE videocards SET spec_1=%s WHERE id=%s;", (spec, i))
        conn.commit()
        i += 1
    
    i = 1

    for spec in spec_2:
        cur.execute(f"UPDATE videocards SET spec_2=%s WHERE id=%s;", (spec, i))
        conn.commit()
        i += 1
    
    i = 1

    for spec in spec_3:
        cur.execute(f"UPDATE videocards SET spec_3=%s WHERE id=%s;", (spec, i))
        conn.commit()
        i += 1

    i = 1

    for spec in spec_4:
        cur.execute(f"UPDATE videocards SET spec_4=%s WHERE id=%s;", (spec, i))
        conn.commit()
        i += 1

    i = 1

    for spec in spec_5:
        cur.execute(f"UPDATE videocards SET spec_5=%s WHERE id=%s;", (spec, i))
        conn.commit()
        i += 1

    i = 1

    for spec in spec_6:
        cur.execute(f"UPDATE videocards SET spec_6=%s WHERE id=%s;", (spec, i))
        conn.commit()
        i += 1
    
    i = 1
    
    cur.close()
    conn.close()

# I had to make parsing and sending data to database
# separate because otherwise it refuses to work
# for some mysterious reason so I recommend you
# to run steps 1-3 separately

# Step 1
parse_names()
time.sleep(5)
parse_images()
time.sleep(5)
send_to_db()

# Step 2
parse_credit_values()
send_credit_to_db()

# Step 3
parce_prices()
send_prices_to_db()
parce_id()
send_id_to_db()
parce_spec()
send_spec_to_db()

driver.quit()
