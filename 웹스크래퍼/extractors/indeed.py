from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
browser = webdriver.Chrome(options=options, executable_path="C:/Users/Kevin De Bruyne/Desktop/파이썬칩/웹스크래퍼/need/chromedriver.exe")

def get_page_count(keyword):
    base_url = "https://kr.indeed.com/jobs?q="
    end_url = "&limit=50"
    browser.get(f"{base_url}{keyword}{end_url}")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("nav", class_="pagination")
    if pagination == None: #페이지가 하나밖에 없는것 = 파지네이션 이퀄 None, 그럼 당연히 return값으로 1을 받아야 함
        return 1
    pages = pagination.find_all("a")
    count = len(pages)
    if count >=5:
        return 5
    else:
        return count


def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    results = []
    for page in range(pages):
        base_url = "https://kr.indeed.com/jobs"
        end_url = "&limit=50"
        final_url = f"{base_url}?q={keyword}&start={page*10}{end_url}"
        print("Requesting", final_url)
        browser.get(final_url)
        
        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_="jobsearch-ResultsList")
        jobs = job_list.find_all('li', recursive=False)
        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find("span", class_="companyName")
                location = job.find("div", class_="companyLocation")
                job_data = {
                    'link' : f"https://kr.indeed.com{link}",
                    'company' : company.string.replace(","," "),
                    'location' : location.string.replace(","," "),
                    'position': title.replace(","," ")
                }
                results.append(job_data)
    return results


