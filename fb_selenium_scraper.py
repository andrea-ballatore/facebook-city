# -*- coding: utf-8 -*-
# Andrea Ballatore
#
# Web scraper for facebook groups

import time
import uuid
import json
import os
import random
import calendar
import datetime
import requests
import sys
import urllib
import traceback
import subprocess
import pandas as pd
import validators
import numpy as np
from webbot import Browser


GROUP_TYPES = ['General group',"Jobs group",'Buy and sell group',
    'Gaming group','Social learning group','Parenting group','Custom group',
    'Teams & projects group','Work group',
    'General',"Jobs",'Buy and sell',
    'Gaming','Social learning','Parenting','Custom',
    'Teams & projects','Work']

GOOGLE_PAUSE_SECS = 3

VPN_SERVERS = ['uk-manchester','uk-london','uk-southampton','ireland','belgium',
                'isle-of-man','luxembourg','austria']

def is_group_type_valid(txt):
    if txt in GROUP_TYPES: return True
    if 'group focus:' in txt.lower(): return True
    return False

def gen_random_page_fn():
    import uuid
    fn = 'tmp/pages_dump/'+str(uuid.uuid4())+'.html'
    return(fn)


def read_file(fn):
    with open(fn, 'r') as content_file:
        content = content_file.read()
        return(content)


# extract numbers from text fields
def extract_int(s, no_string):
    import re
    if no_string and no_string in s.lower():
        i = 0
    else: i = int(re.findall(r'\d+', s.replace(',',''))[0])
    assert i >= 0
    return i


# extract numbers from text fields
def extract_hum_number(s):
    s = s.lower()
    import re
    numbs = re.findall(r"[-+]?\d*\.\d+|\d+",s)
    if len(numbs) == 0: 
        return None

    assert len(numbs)==1
    flnum = float(numbs[0])

    if 'k' in s:
        flnum = flnum * 1e3
    if 'm' in s:
        flnum = flnum * 1e6

    return(flnum)


def extract_fb_data_from_fb_page(html, fn):
    from bs4 import BeautifulSoup
    print('extract:', fn)
    group_uid = fn.replace('.html','').replace('tmp/pages_dump_fb/','')
    #if group_uid != 'fbgr_001619' and group_uid != 'fbgr_000757':
    #    return None
    #print(group_uid)

    def _get_idx_from_data(data, match, exact=False):
        for mod_idx, di in enumerate(data):
            if exact:
                if match.lower() == di.lower(): 
                    return mod_idx
            elif match.lower() in di.lower():
                return mod_idx
        return -1

    if "this content isn't available at the moment" in html.lower() or "something went wrong" in html.lower() or \
        "the link you followed may be broken" in html.lower():
        print("Deleted/empty group",fn)
        df = pd.DataFrame({'group_uid':[group_uid], 'found':[False], 'html_file':[fn]}, index=[group_uid])
        return df
    
    soup = BeautifulSoup(html, 'html.parser')

    INFO_QUERY = 'div.jroqu855.nthtkgg5'
    res = soup.select(INFO_QUERY)
    if len(res) == 0: 
        raise Exception('data not found in page',fn)
    
    i = -1
    res_data = []
    for el in res:
        i += 1
        for subel in el:
            dataitem = subel.get_text('\t').strip()
            if dataitem:
                res_data.append(dataitem)
    #print(res_data)
    del i
    print('data items n =',len(res_data))
    assert len(res_data) >= 16, "too few data items: {}".format(len(res_data))

    # check for tags
    tags_idx = _get_idx_from_data(res_data, 'Tags', True)
    tags = None
    if tags_idx > 6:
        # tags found, remove them
        # pop two elements tags
        res_data.pop(tags_idx)
        if res_data[tags_idx]!='History':
            tags = res_data.pop(tags_idx)
        else: 
            print('empty tags found')

    # fill gaps in data
    if not res_data[3].lower() in ['public','private']:
        # missing description
        res_data.insert(2, 'no description')

    if res_data[8].lower() == 'history':
        # missing place
        res_data.insert(7, 'no place')

    if res_data[12].lower() == 'activity':
        # missing place
        res_data.insert(12, 'no admin')

    # extract all fields


    #print(res_data)
    group_name = res_data[0].strip()
    desc = res_data[2].strip()
    priv = res_data[3].strip()

    assert priv in ['Private','Public'], 'invalid private/public attr'
    vis = res_data[5].strip()
    hist_idx = _get_idx_from_data(res_data, 'History', True)
    gtype = res_data[hist_idx-1].strip()
    assert is_group_type_valid(gtype), 'invalid group type: '+gtype

    place_str = res_data[7].strip()

     # extract date
    import dateutil.parser
    hist_idx = _get_idx_from_data(res_data, 'History', True)
    assert hist_idx > 7, "invalid hist_idx {}".format(hist_idx)
    creation_date_str = res_data[hist_idx+1].strip()
    assert 'Group created' in creation_date_str
    creation_date_str2 = creation_date_str.replace('Group created on','')
    creation_date_str2 = ' '.join(creation_date_str2.replace('See more','').strip().split(' ')[0:3])
    creation_date = dateutil.parser.parse(creation_date_str2, fuzzy_with_tokens=True)[0]
    #return pd.DataFrame() # DEBUG

    # activity stats
    act_idx = _get_idx_from_data(res_data, 'Activity', True)
    members_str = res_data[act_idx + 3].strip()
    members_n = extract_int(members_str, None)
    assert members_n > 0 and members_n < 5*10000*10000
    lastmonth_posts_str = res_data[act_idx + 2].strip()
    lastmonth_posts = extract_int(lastmonth_posts_str, 'no posts')
    week_members_str = res_data[act_idx + 4].strip()
    week_members_new = extract_int(week_members_str, 'no new ')
    dailyposts_str = res_data[act_idx + 1].strip()
    dailyposts = extract_int(dailyposts_str, 'no new post')

    # find moderation rules
    mod_str = None
    mod_idx = _get_idx_from_data(res_data, 'Group rules from the admins')
    if mod_idx is not None:
        # extract moderation
        mod_str = '\t'.join(res_data[mod_idx+1:])

    # build result
    infodf = pd.DataFrame({'group_uid':[group_uid],
                'group_name':[group_name],
                'description': [desc],
                'privacy':[priv],
                'found':[True],
                'html_file':[fn],
                'visibility':[vis],
                'creation_date_str':[creation_date_str],
                'creation_date':[creation_date],
                'creation_year':[creation_date.strftime('%Y')],
                'creation_yymm':[creation_date.strftime('%Y-%m')],
                'fb_place':[place_str],
                'group_type':[gtype],
                'group_tags': [tags],
                'members_str':[members_str],
                'members_n':[members_n],
                'week_members_str':[week_members_str],
                'week_members_new':[week_members_new],
                'lastmonth_posts_str':[lastmonth_posts_str],
                'lastmonth_posts':[lastmonth_posts],
                'dailyposts_str':[dailyposts_str],
                'dailyposts':[dailyposts],
                'group_rules_str':[mod_str],
                'group_name2':[group_name],
                'description2': [desc],
                'group_uid2':[group_uid]
            }, index=[group_uid])
    return(infodf)


def extract_fb_links_from_google_page(html, fn):
    from bs4 import BeautifulSoup    
    soup = BeautifulSoup(html, 'html.parser')

    place_code = fn.replace('.html','').replace('tmp/pages_dump/','')
    links = []
    for a_tag in soup.find_all("a"):
        href = a_tag.attrs.get("href")
        links.append(href)
    
    # keep only fb links
    links = [clean_group_url(l) for l in links if is_fb_link(l)]
    links = [l for l in links if len(l) > 10] # remove empty string
    links = pd.Series(links).drop_duplicates().tolist() # get unique

    if len(links) == 0: 
        return None

    # build results
    ids = [place_code+'_'+'{:03d}'.format(l+1) for l in range(len(links))]
    granks = range(1,len(links)+1)
    assert len(granks)==len(links) and len(granks)==len(links) and len(ids)==len(links)

    df = pd.DataFrame({'place_code': place_code, 'google_rank': granks,
        'html_file': fn,'url':links},index=ids)
    assert len(df.index)==len(links)
    return df


def write_file( content, fn ):
    file1 = open(fn,"w") #write mode 
    file1.write(content) 
    file1.close() 


def get_url( url, session ):
    p = session.get( url )
    print(p.content)


def random_sleep(min=0,max=2):
    n = random.randint(min*1000,max*1000)/1000 
    print("\trandom_sleep secs",n)
    time.sleep( n )


# l = d m y
def format_date_lexis(dd):
    s = str(dd.day)+'%2F'+str(dd.month)+'%2F'+str(dd.year)
    return(s)


def get_last_day_month(y,m):
    import calendar
    assert m in range(1,13,1)
    last_day = calendar.monthrange(y,m)[1]
    return(last_day)


def load_list_from_file(fn):
    cont = read_file(fn).strip()
    #print(cont)
    lcont = cont.split('\n')
    # remove commented lines
    import re
    out = []
    for l in lcont:
        m = re.match(r'^([^#]*)#(.*)$', l)
        if m:  # The line contains a hash / comment
            l = m.group(1)
        else: out.append(l)
    out = [x for x in out if x]
    return(out)


def get_timestamp():
    import datetime
    return(str(datetime.datetime.now()))

# =============== MAIN =============== #

# set VARIABLES

def tests():
    web = Browser()
    # END TESTS


def get_fb_page(web, url):
    print("get_fb_page", url)
    while True:
        try:
            random_sleep(0,1)
            web.go_to(url)
            random_sleep(0,1)
            tmp_html = web.get_page_source()
            # detect scraping issues
            if 'you must log in to continue' in tmp_html.lower() or 'redirected you too many times' in tmp_html.lower():
                raise Exception('Facebook is blocking: '+url)
            if 'your request couldn''t be process' in tmp_html.lower():
                raise Exception('Facebook didn''t respond: '+url)
            # close cookie popup
            if 'allow essential and optional cookies' in tmp_html.lower():
                web.click('allow essential and optional cookies', tag='span')

            n = tmp_html.lower().count('see more')
            if n > 2:
                web.click('See more', tag='div', multiple = True)
            random_sleep(0.2,1)
            html = web.get_page_source()
            return web,html
        except Exception as e:
            print(e)
            print('failed to download page, changing VPN')
            web.quit()
            vpn_random_region()
            random_sleep(1,1)
            web = Browser()
            #web = Web # init_google_browser()
            random_sleep(2,3)


def gen_google_url(query_str):
    n_results = 50
    query_enc = urllib.parse.quote_plus(query_str)
    url = 'https://www.google.co.uk/search?q='+query_enc+'&num='+str(n_results)+'&hl=en-GB'
    print(url)
    return url


def run_google_query(web, querytext):
    assert len(querytext)>3
    print("run_google_query", querytext)
    # get google url
    queryurl = gen_google_url(querytext)

    if True: # run webbot
        web.go_to(queryurl)
        #web.type(querytext, classname="form-input", number=1)
        #random_sleep(0,1)
        #web.click('Google Search', classname="form-input", number=2)
        #web.press(web.Key.TAB)
        random_sleep(1,3)
        web.press(web.Key.ENTER)
        random_sleep(GOOGLE_PAUSE_SECS,GOOGLE_PAUSE_SECS*1.5)
        html = web.get_page_source()
    else:
        # run VPN url
        random_sleep(0,2)
        html = get_url_vpn(queryurl)

    if 'unusual traffic from your computer network' in html.lower():
        raise Exception('Google is blocking. '+querytext)

    return html


def click_on_google_eula(web):
    print("click_on_google_eula")
    random_sleep(1,2)
    # clear user agreement
    web.press(web.Key.TAB)
    random_sleep(0,1)
    #web.press(web.Key.TAB)
    #random_sleep(1,2)
    web.press(web.Key.ENTER)
    random_sleep(0,1)


def get_url_vpn(url):
    pia_socks5 = 'OMITTED'
    proxies = {'http': pia_socks5,'https': pia_socks5}
    r = requests.get(url, proxies=proxies )
    if r.status_code == 429: 
        raise Exception("429 Too Many Requests")
    assert r.status_code == 200, 'failed to download '+str(r.status_code) + ' ' + url
    return r.text

def restart_browser(web):
    web.quit()

def init_google_browser():
    from webbot import Browser
    web = Browser()
    start_url = "https://www.google.co.uk/"
    random_sleep(0,1)
    web.go_to(start_url)
    click_on_google_eula(web)
    random_sleep(0,2)
    return web

def vpn_off():
    ret = run_os_command('piactl disconnect')
    print(ret)

def vpn_on():
    ret = run_os_command('piactl connect')
    print(ret)

def vpn_go_region(reg):
    assert reg in VPN_SERVERS
    ret = run_os_command('piactl set region '+reg)
    print(">> vpn_go_region:",reg)
    return ret

def run_os_command(cmd):
    ret = subprocess.check_output(cmd, shell=True)
    ret = ret.decode("utf-8").strip()
    return ret

def is_fb_link(url):
    if not url: return False
    if url == '': return False
    b = 'facebook.com/groups/' in url
    b = b and not ('webcache.googleusercontent.com' in url)
    b = b and not ('translate.google.' in url)
    return b

def vpn_random_region():
    vpn_go_region(random.choice(VPN_SERVERS))

def vpn_is_on():
    ret = run_os_command('piactl get connectionstate') == 'Connected'
    return ret

def scrape_google_london_place_groups(topicsdf):
    # NOTE: this function needs PIA VPN to work
    assert vpn_is_on(),'VPN must be on'

    # init browser and google settings
    web = init_google_browser()
    
    outdf = pd.DataFrame()
    # scan place names
    for index, row in topicsdf.iterrows():
        place_id = row['place_code'].strip()
        fn = 'tmp/pages_dump/'+place_id+'.html'
        if os.path.isfile(fn):
            print('file found, skip')
            continue
        
        print(index,row)
        if index % 1000 == 0:
            print("long pause idx=",index)
            random_sleep(60,600)
        
        query = row['place_name'].strip() + " site:en-gb.facebook.com/groups"
        
        # get data from google
        found = False
        while not found:
            try: 
                html = run_google_query(web, query)
                found = True
            except Exception as e:
                print(e)
                print('failed to download page, changing VPN')
                web.quit()
                vpn_random_region()
                random_sleep(1,1)
                web = init_google_browser()
                random_sleep(2,2)
        
        write_file(html, fn)
        outdf = pd.concat([outdf, pd.DataFrame({'google_query': [query],'file':fn},
                       index=[place_id])])
        print("\t", fn)
    dffn = 'tmp/scraping_google_out.csv'
    outdf.to_csv(dffn, index_label="place_code")
    print("scraping complete.",dffn)
    return


def extract_fbgroup_info(foldfn):
    print("extract_fbgroup_info", foldfn)
    import glob
    outdf = pd.DataFrame()
    i = 0
    
    for fn in glob.glob(foldfn+"/*.html"):
        i += 1
        if i % 100 ==0: print('\t',i)
        html = read_file(fn)

        page_df = extract_fb_data_from_fb_page(html, fn)
        assert page_df is not None, fn
        outdf = pd.concat([outdf, page_df])
        
    outfn = 'tmp/fb_groups_info_df'
    print(outfn)
    # save files
    outdf.to_csv(outfn+'.tsv', index=False, sep='\t')
    #outdf.to_excel(outfn+'.xlsx', index_label='row_id')
    outdf.to_pickle(outfn+'.pik')


def extract_google_results(foldfn):
    print("extract_google_results", foldfn)
    import glob
    outdf = pd.DataFrame()
    i = -1
    for fn in random.shuffle(glob.glob(foldfn+"/*.html")):
        i += 1
        
        html = read_file(fn)
        if "did not match any documents" in html.lower():
            # empty results from Google
            print(">> No results in ",fn)
            continue
        # extract data from html
        page_df = extract_fb_links_from_google_page(html, fn)
        if page_df is not None:
            # build results
            outdf = pd.concat([outdf, page_df])
        else: 
            print('No FB links found in', fn)
    outfn = 'tmp/fb_groups_from_google.csv'
    print(outfn)
    outdf.to_csv(outfn,index_label='row_id')


def clean_group_url(url):
    # extract Facebook group url
    import re
    url = url.replace('/url?q=','')
    
    if url[0:3]=='/se': return ''
    idx = [m.start() for m in re.finditer('/', url)]
    if len(idx) < 5: return ''
    end_str = idx[4]
    return url[0:end_str]


def analyse_facebook_groups_info(fn_pik):
    print("analyse_facebook_groups_info",fn_pik)
    df = pd.read_pickle(fn_pik)
    print(len(df))
    print(df.info())
    print(df.describe())
    

def scrape_facebook_groups_info(fn):
    print("scrape_facebook_groups_info")
    df = pd.read_csv(fn, sep='\t')
    print(len(df), df.columns)
    #group_unique_urls = sorted(df["url"].unique())
    #print(len(group_unique_urls))
    offset = 0
    if len(sys.argv) >= 2:
        offset = int(sys.argv[1])
        print('offset', offset)
    
    from webbot import Browser
    
    web = Browser()
    
    if offset > 0:
        df = df.tail(offset) # this is used to split jobs
    
    for index, row in df.sample(frac=1).iterrows():
        print(index)

        fout = "tmp/pages_dump_fb/" + row['fb_url_id'] + '.html'
        assert os.path.normpath(fout), fout + ' is not a valid path'
        # form and validate group URL
        if row['url'][-1]=='/':
            url = row['url']+'about'
        else:
            url = row['url']+'/about'
        
        assert validators.url(url), url
        if not 'facebook.com/groups/' in url:
            continue

        if os.path.isfile(fout):
            print('file found, skip')
            continue

        # get facebook page and save it
        print(url)
        web,html = get_fb_page(web, url)
        write_file(html,fout)
        print(fout)


def main():
    print("\n>>>> Scrape data >>>>\n")
    # set up folders
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
        os.makedirs("tmp/pages_dump")
    if not os.path.exists("tmp/pages_dump_fb"):
        os.makedirs("tmp/pages_dump_fb")

    # load input     
    topics = pd.read_csv('data/input/london_placenames-v2.csv')
    print('>> Topics to scrape:',len(topics))
    
    try:
        if False: # step 1
            # scrape Google
            scrape_google_london_place_groups(topics)
        if False: # step 2
            # extract Facebook data from Google pages
            extract_google_results("tmp/pages_dump")
        if False: # step 3
            # scrape Facebook groups to HTML dump
            scrape_facebook_groups_info("data/facebook_city_data/fb_groups_urls.tsv")
        if True: # step 4
            # extract Facebook group info from HTML dump
            extract_fbgroup_info("tmp/pages_dump_fb")
        if False: # step 5
            # analyse Facebook groups
            analyse_facebook_groups_info("tmp/fb_groups_info_df.pik")
        
        # ==== the rest of the analysis is done in R ==== 

        print('OK')
    except Exception as e:
        print(e.with_traceback)
        print(e)
        print("Script failed.")

    
if __name__ == '__main__':
    main()
