import requests
import argparse
import sys
import os
import re
def request_url_show_error(url,proxy):
    try:
        if proxy == "":
            #print "proxy blank"
            r = requests.get(url)
        else:
            #print "Proxy with data"
            r = requests.get(url,proxies=(proxy))
        #check if 200 OK then size of response more 0
        #check if 500 error
        #check if 200 with error or  error
        if 200 == r.status_code:
            default="0"
            if 0 != int(r.headers.get('content-length',default)):
                error_list="(notice|warning|parse|fatal|error)"
                if re.search("Index of",r.text, re.IGNORECASE):
                    print "Directory Listing at ; " + url
                elif re.search(error_list,r.text, re.IGNORECASE):
                    #print "Response With Error ; " + url + " ; " + str(r.status_code) + " ; " + r.headers['content-length'] + " ; " + r.text.replace('\n', '')
                    print "Response With Error ; " + url + " ; " + str(r.status_code) + " ; " + r.headers['content-length']
                else:
                    print "Response Need Check ; " + url + " ; " + str(r.status_code) + " ; " + r.headers['content-length']


        else:
            print "Invalid Status  Code ;" + url + " Status " + str(r.status_code)
    except Exception as e:
        print "Error in ; " + url + str(e)
        pass

def recursive_list(folder,target,proxy):
    #print "CURRENT FOLDER : " + folder
    for x in os.listdir(folder):
        modi=""
        #print "A :" + folder + ": Seperator :" + os.path.sep + ": Folder :" + x
        if os.path.isdir(os.path.join(folder , x)):
            modi="/"
            #print "Dir Found : " + target + x + modi
            recursive_list(folder + modi + x,target + x + modi,proxy)
            #uncomment to show Directory names
            #print target + x + modi
        #uncomment to show files names
        #print target + x
        fileName, fileExtension = os.path.splitext(target + x)
        if ".js" != fileExtension and ".css" != fileExtension and ".gif" != fileExtension and ".jpg" !=fileExtension:
            #print target + x
            request_url_show_error(target + x,proxy)
    #print "Moving Out of :" + folder
    

def main(argv):
    desc="""This program is used to  identify various error that occur when php files are executed out of order or when they are executed directly"""
    epilog="""Credit (C) Anant Shrivastava http://anantshri.info"""
    parser = argparse.ArgumentParser(description=desc,epilog=epilog)
    parser.add_argument("--url",help="Provide URL",dest='target',required=True)
    parser.add_argument("--proxy",help="Provide HTTP Proxy in http(s)://host:port format", dest='proxy',required=False)
    parser.add_argument("--folder",help="Provide Local Directory", dest='fold',required=True)
    x=parser.parse_args()
    target=x.target
    folder=x.fold
    prox=x.proxy
    proxy_dict=""
    if prox != "":
        print "Proxy Defined"
        proxy_dict = {"http":prox}
    else:
        print "Proxy not defined"
        proxy_dict = ""
    print "Comment : URL : Status Code : Error Message"
    recursive_list(folder,target,proxy_dict)
    #print os.listdir(folder)
    
    
        
if __name__ == "__main__":
    main(sys.argv[1:])
