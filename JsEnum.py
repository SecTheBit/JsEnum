import requests,re
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse
from termcolor import colored
import sys
count=0
header = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    } # header is necessary for bypassing the restrictions ## change it accordingly
sensitive_keywords=["aws-keys","aws","firebase","s3-buckets","ip","token","auth_key","password","credentials"] #Add your sensitive keywords here

def Filewrite(list,url,count):
    domain_name= urlparse(url).netloc
    string_s=" "
    file_name=string_s.join(domain_name)
    count=str(count)
    name=file_name+count+".txt"
    new_file_path=open(name,"a")
    for js_urls in list:
        
        if "www" in js_urls and js_urls.startswith("//"):
                js_urls="https:"+js_urls

        if "www" in js_urls and js_urls.startswith("/"):
            js_urls="https:/"+js_urls

        if (domain_name not  in js_urls and "www" not in js_urls) and (js_urls.startswith("//")):
            js_urls.replace("//","/")
            js_urls="https://"+domain_name+js_urls

        else:
            if (domain_name  not  in js_urls and "www" not in js_urls) and (js_urls.startswith("/")):
                 js_urls="https://"+domain_name+js_urls
            else:
                if(domain_name  not  in js_urls and "www" not in js_urls) and (js_urls.startswith("https:")):
                 js_urls=js_urls
        new_file_path.write(js_urls+"\n")
    new_file_path.close()
    FindingSensitiveInfo(name)

def ExtractJslinks(url,count):
    links_list=[]
    count_s=0
    try:
        response=requests.get(url,headers=header)
    except requests.exceptions.RequestException as e:
        print (colored("[+] Some Error Occured While Fetching the url :"+urls,'red'))
    page_html=BS(response.text, 'html.parser')
    for scripts in page_html.find_all("script"):
        links=scripts.get("src")
        if(links==None):
          continue
        else:
            count_s=count_s+1
            links_list.append(links)

    print("[+] Found Total "+str(count_s)+" Js Links in the Url "+url)
    Filewrite(links_list,url,count)

def FindingSensitiveInfo(file):
    print (colored("[+]====================Started Finding Sensitive Keywords==========================[+]",'yellow'))
    file_tmp=open(file,"r")
    for urls in file_tmp:
        urls=urls.strip()
        try:
            response=requests.get(urls,headers=header)
        except requests.exceptions.RequestException as e:
            print (colored("[+] Some Error Occured While Fetching the url :"+urls,'red'))
        for keywords in sensitive_keywords:
            if keywords in response.text:
                print (colored("[+]The Keyword: "+keywords+" is found in the url: "+urls,'green'))

    file_tmp.close()

def FileRead(file_of_urls):
    i=0
    try:
        file=open(file_of_urls,"r")
    except requests.exceptions.RequestException as e:
        print (colored("[+] Some Error Occured in the file :"+file_of_urls,'red'))
        raise SystemExit(e)
    for url in file:
        print(colored("\n[+]URL Grepped: "+url,'cyan'))
        url=url.strip()
        i=i+1
        ExtractJslinks(url,i)
    file.close()

def main():
    file_of_urls=sys.argv[1]
    FileRead(file_of_urls)

if __name__=="__main__":
    main()
