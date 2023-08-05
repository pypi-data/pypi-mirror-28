from __future__ import print_function
import boto3
import requests
from botocore.exceptions import ClientError
# from subdomain.mysubdomain import findsubdomain
from thread import start_new_thread, allocate_lock
from threading import Thread, Lock
import logging
import time
from datetime import datetime
# from argparse import ArgumentParser

# Important variables
domains = []
old_domains = []
newly_added_domains = []
subdomains = []
old_subdomains = []
newly_added_subdomains = []
hijackable_subs = []
old_hijackable_subs = []
newly_added_hijackable_subs = []
end_points = []
old_end_points = []
newly_added_endpoints = []
in_path = ['domains', 'subdomains', 'hijackable_subdomains', 'endpoints']

# works like a mutex
# first index is the default maximum thread count
# second index is the current running threads count
thread_counter = [10, 0]

# lock that will be acquired when checking if thread can be initiated or not
lock_while = allocate_lock()

# lock that will be acquired when the request has fetched result for
lock_write_sdcfcr = allocate_lock()

# lock will be acquired when accessing hijackable_subs
lock_write_hs = allocate_lock()
################################################


def compare(old, newer):
    '''
    compares 2 arrays. finds if there are any entry in "newer" list thata re not in "old" list and fills them in mDiff.
    :param old: list of records
    :param newer: list fo records
    :return: Returns mDiff
    '''
    mDiff = []
    if len(old) > 0 and len(newer) > 0:
        for d in newer:
            if d not in old: mDiff.append(d)
    return mDiff


def get_domains_and_subdomains_from_aws():
    '''
    gets domains and subdomains from aws
    :return: sets 2 global variables "domains" and "subdomains"
    '''
    logging.info('get_domains_and_subdomains_from_aws Started')
    try:
        logging.info('Connecting to Route53...')
        aws_client = boto3.client('route53')
        logging.info('Connection to Route53 Successful')
        logging.info('Fetching all domains...')
        next_marker = ''
        doms = []
        while next_marker is not None:
            if next_marker == '':
                temp = (aws_client.list_hosted_zones())
            else:
                logging.info('Fetching again because more than 100 items')
                temp = (aws_client.list_hosted_zones(Marker=next_marker))
            for domain in temp['HostedZones']:
                doms.append(domain)
            try:
                next_marker = temp['NextMarker']
            except KeyError:
                logging.info('KeyError Occurred. But, chill, it"s okay. It"s supposed to do so')
                next_marker = None
        logging.info('Fetched all domains')

        subs = []
        # with open(appendThisWithOutputFileName + '-subdomains.csv', 'w') as outFile:
        # For each domain
        for domain in doms:
            logging.info('Fetching all subdomains for: ' + domain['Name'][:-1] + '...')
            next_record_identifier = ''
            # get all records of a domain
            while next_record_identifier is not None:
                if next_record_identifier == '':
                    temp = aws_client.list_resource_record_sets(HostedZoneId=domain['Id'], MaxItems="100")
                else:
                    temp = aws_client.list_resource_record_sets(HostedZoneId=domain['Id'], MaxItems="1",
                                                                NextRecordIdentifier=next_record_identifier)
                # print all records fetched in this iteration for this domain
                for record in temp['ResourceRecordSets']:
                    mStr = record['Name']
                    if mStr[-1] == '.': mStr = mStr[:-1]
                    subs.append(mStr)
                # if record set is greater than 100 for a domain, this won't work
                try:
                    next_record_identifier = temp['NextRecordIdentifier']
                except KeyError:
                    logging.info('KeyError Occurred. But, chill, it"s okay. It"s supposed to do so')
                    next_record_identifier = None
        subdomains = list(set(subs))
        domains = [i['Name'][:-1] for i in doms]
    except ClientError as e:
        print(e)
        logging.warning('Couldn"t get anything from AWS. Returning empty lists. This could possibly lead to error in next steps')
        logging.info('get_domains_and_subdomains_from_aws Finished')
        return [], []
    logging.info('get_domains_and_subdomains_from_aws Finished')
    return domains, subdomains


def get_subdomains_from_shodan_google(doms, subs):
    '''
    takes domains and subdomains lists as parameters and finds publicly available subdomains against a each domain name, usign nmap, dnscan and aquatone.
    :param doms:
    :param subs:
    :return: appends newly found subdomians to global variable "subdomains"
    '''
    # get subdomains from PT team's module
    # for all domains
    global subdomains
    for domain in doms:
        # get subdomains from PT Team's module
        for d in findsubdomain(domain):
            # add to the subdomains list
            if len(d) > 0: subdomains.append(d)
        subdomains = list(set(subdomains))
    # return subdomains


# This function will return previously written domains and subdomains
# from files 'domains' and 'subdomains' in the same directory
def get_old_data(in_path):
    '''
    reads old records from files at in_path
    :param in_path:
    :return:
    '''
    logging.info('get_old_data Started')
    try:
        with open(in_path) as inFile:
            temp = []
            for i in inFile.readlines():
                temp.append(str(i).replace('\n', ''))
        if temp[-1] == '': temp = temp[:-1]
        if len(temp) > 0:
            logging.info('get_old_data Finished')
            return temp
        else:
            logging.info('Couldn"t read from file: ' + in_path)
            logging.info('get_old_data Finished')
            return []
    except:
        logging.info('Couldn"t read from file: ' + in_path)
        logging.info('get_old_data Finished')
        return []


def get_hijackable_subs(subdomains, num_of_threads=10):
    '''
    takes list of subdomains and num of threads to create 1 request per thread and check if subdomain can be hijacked
    :param subs: list of subdomians
    :param num_of_threads: default number of threads to be used
    :return:
    '''
    logging.info('get_hijackable_subs Started')
    if subdomains == None:
        logging.warning('Returning because no subdomains in list "subdomains". Could lead to error')
        return
    thread_counter[0] = num_of_threads
    thread_counter[1] = num_of_threads
    for d in subdomains:
        # acquire lock to decrement thread counter before starting thread
        logging.info('Acquiring lock')
        lock_while.acquire()
        while thread_counter[1] < 1:
            # Do nothing while all threads are busy
            time.sleep(1)
        logging.info('Thread counter: ' + str(thread_counter[1]))
        logging.info('\n\n\n\n\n\n\n')
        thread_counter[1] -= 1
        lock_while.release()
        logging.info('Released lock')

        logging.info('Started new thread')
        start_new_thread(check_subdomain_hijacking, (d,))

    # keep the whole process paused here until all the values have returned
    logging.info('Main gonna wait')
    while(thread_counter[0] != thread_counter[1]):
        pass

    logging.info('get_hijackable_subs Finished')
    return hijackable_subs


def check_available_endpoints(subdomains, num_of_threads=10):
    '''
    checks for each subdomain if known endpoints exist
    :return:
    '''
    logging.info('check_available_endpoints Started')
    thread_counter[0] = num_of_threads
    thread_counter[1] = num_of_threads
    global lock_while, lock_write_sdcfcr, lock_write_hs
    lock_while = Lock()
    lock_write_sdcfcr = Lock()
    lock_write_hs = Lock()
    mThreads = []
    global end_points
    for d in subdomains:
        # eps = check_endpoints(d)

        logging.info('Acquiring Lock')
        lock_while.acquire()
        logging.info("Can't start thread")
        while thread_counter[1] < 1:
            time.sleep(2)
            logging.info('Thread counter: ' + str(thread_counter[1]))
            logging.info('\n\n\n\n\n\n\n')
        logging.info('Can start Thread')
        thread_counter[1] -= 1
        lock_while.release()
        logging.info('Released Lock')

        logging.info('Starting new thread for subdomain: ' + d)
        t = Thread(target=check_endpoints, args=(d,))
        mThreads.append(t)
        mThreads[-1].start()

    for t in mThreads:
        logging.info('Gonna wait for this thread')
        t.join()


        # if len(eps) > 0: end_points = end_points + eps
    # end_points = list(set(end_points))
    logging.info('check_available_endpoints Finished')
    return end_points


def write_list_to_file(mList, output_path):
    '''
    Takes a list and write it to specified output_path after appending \n with every line
    :param mList: list of data
    :param output_path: path to output file
    :return:
    '''
    logging.info('write_list_to_file Started')
    if mList is not None:
        if len(mList) == 0:
            with open(output_path, 'w') as outFile:
                logging.info('Emptying File: ' + outFile.name)
                pass
        elif len(mList) > 0:
            with open(output_path, 'w') as outFile:
                for i in mList:
                    outFile.write(i + '\n')
    logging.info('write_list_to_file Finished')


def check_subdomain_hijacking(subdomain):
    '''
    function that takes a subdomain and checks if it contains vulnerable content to identify whether it is hijackable or not
    :param subdomain: subdomain name
    :return: true or false in can_be_hijack, whether domain can be hijacked or not
    '''
    logging.info('check_subdomain_hijacking Started')
    VulnContents = ["<strong>Trying to access your account", "Use a personal domain name",
                    "The request could not be satisfied",
                    "Sorry, We Couldn't Find That Page", "Fastly error: unknown domain",
                    "The feed has not been found",
                    "You can claim it now at", "Publishing platform",
                    "There isn't a GitHub Pages site here",
                    "No settings were found for this company",
                    "Heroku | No such app", "<title>No such app</title>",
                    "You've Discovered A Missing Link. Our Apologies!",
                    "Sorry, couldn&rsquo;t find the status page", "NoSuchBucket",
                    "Sorry, this shop is currently unavailable",
                    "<title>Hosted Status Pages for Your Company</title>",
                    "data-html-name=\"Header Logo Link\"",
                    "<title>Oops - We didn't find your site.</title>",
                    "class=\"MarketplaceHeader__tictailLogo\"",
                    "Whatever you were looking for doesn't currently exist at this address",
                    "The requested URL was not found on this server",
                    "The page you have requested does not exist",
                    "This UserVoice subdomain is currently available!",
                    "but is not configured for an account on our platform",
                    "<title>Help Center Closed | Zendesk</title>",
                    "Sorry, We Couldn't Find That Page Please try again",
                    "cloudfront", "heroku", "there is no app configured at that hostname",
                    "herokucdn.com/error-pages/no-such-app.html", "nosuchbucket",
                    "here isn't a github pages site here", "sorry, this shop is currently unavailable",
                    "whatever you were looking for doesn't currently exist at this address.",
                    "the site you were looking for couldn't be found",
                    "this domain is successfully pointed at wp engine, but is not configured for an account on our platform",
                    "fastly error: unknown domain",
                    "the gods are wise, but do not know of the site which you seek.",
                    "sorry, we couldn't find that page", "help center closed",
                    "oops - we didn't find your site.",
                    "we could not find what you're looking for.",
                    "no settings were found for this company:",
                    "the specified bucket does not exist",
                    "the thing you were looking for is no longer here, or never was",
                    "if you're moving your domain away from cargo you must make this configuration through your registrar's dns control panel.",
                    "the feed has not been found.", "may be this is still fresh!",
                    "this uservoice subdomain is currently available!",
                    "sites.google.com"]

    can_be_hijack = False
    known_appends = ['http://', 'https://']
    urls = [i+subdomain for i in known_appends]
    # url = "http://" + subdomain

    for url in urls:
        logging.info('Checking for vulnerable content in: ' + url)
        try:
            res = requests.get(url, timeout=5)
            for text in VulnContents:
                if text.lower() in res.content.lower():
                    can_be_hijack = True
                    logging.info("This Domain can be hijacked: \t\t------------------> {}".format(url))

                    logging.info('Acquiring lock')
                    lock_write_hs.acquire()
                    logging.info('Appending to subdomains: ' + url)
                    hijackable_subs.append(url)
                    lock_write_hs.release()
                    logging.info('Released lock')
                    break
        #TODO Add proper exception handling
        except Exception as e:
            logging.warning('Some exception occurred: ')
            logging.warning(e)
            # print (e)

    lock_write_sdcfcr.acquire()
    thread_counter[1] += 1
    lock_write_sdcfcr.release()
    logging.info('check_subdomain_hijacking Finished')
    return can_be_hijack


def check_endpoints(domain):
    '''
    takes a subdomain and appends known endpoint names with it and check if those endpoints exist or nor
    :param domain: subdomain name
    :return:
    '''
    logging.info('check_endpoints Started')
    global end_points
    end_points_local = ["/env", "/dump", "/metrics", "/configprops", "/beans", "/autoconfig", "/health",
                  "/heapdump",
                  "/trace", "/mappings", "/cors",
                  "/hystrix.stream", "/actuator", "/auditevents", "/flyway", "/info", "/loggers",
                  "/liquibase", "/docs",
                  "/jolokia", "/logfile", "/management"]

    fp = ["<title>404 Not Found</title>", "<!DOCTYPE html>", "Get Lost",
          "grep -iR cloudfront | cut -d':' -f1 | xargs rm",
          "<h1>502 Bad Gateway</h1>", "message: Not found", "<!DOCTYPE html PUBLIC", "Yahoo"]

    # found_endpoint = []
    for ep in end_points_local:
        url = "http://" + domain + ep
        try:
            logging.info("Checking: " + url)
            res = requests.get(url, timeout=5)
            temp = False
            for f in fp:
                if f in res.content:
                    temp = True
                    break

            if not temp:
                logging.info('Aquiring Lock')
                lock_write_hs.acquire()
                logging.info('Endpoint found ------------------------------------> : ' + url)
                end_points.append(url)
                end_points = list(set(end_points))
                thread_counter[1] += 1
                lock_write_hs.release()
                logging.info('Released Lock')
        #TODO add proper exception hanling
        except:
            logging.info("Not found -> " + url)
    logging.info('check_endpoints Finished')
    # return found_endpoint


def fetch_and_compare_old_data():
    '''
    fetches old records written to files regarding domains, subdomians, hijackable domains and endpoints and compares
    that data with results from now
    :return:
    '''
    # # Compare changed entries
    logging.info('fetch_and_compare_old_data Started')
    global old_hijackable_subs, old_end_points, old_domains, old_subdomains
    old_domains = get_old_data(in_path[0])
    old_subdomains = get_old_data(in_path[1])
    old_hijackable_subs = get_old_data(in_path[2])
    old_end_points = get_old_data(in_path[3])

    if len(old_domains) == 0 or len(old_subdomains) == 0:
        logging.warning('Old Domains and Subdomains fields are empty')
    else:
        global newly_added_domains, newly_added_subdomains, newly_added_hijackable_subs, newly_added_endpoints
        newly_added_domains = compare(old_domains, domains)
        newly_added_subdomains = compare(old_subdomains, subdomains)
        newly_added_hijackable_subs = compare(old_hijackable_subs, hijackable_subs)
        newly_added_endpoints = compare(old_end_points, end_points)
    logging.info('fetch_and_compare_old_data Finished')


def write_to_files():
    '''
    writes current records as well as new/diff records to files
    :return:
    '''
    logging.info('write_to_files Started')
    write_list_to_file(domains, in_path[0])
    write_list_to_file(subdomains, in_path[1])
    write_list_to_file(hijackable_subs, in_path[2])
    write_list_to_file(end_points, in_path[3])

    write_list_to_file(newly_added_domains, 'new-' + in_path[0])
    write_list_to_file(newly_added_subdomains, 'new-' + in_path[1])
    write_list_to_file(newly_added_hijackable_subs, 'new-' + in_path[2])
    write_list_to_file(newly_added_endpoints, 'new-' + in_path[3])
    logging.info('write_to_files Finished')


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    mTime = []
    mTime.append(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))
    logging.info(mTime[0])
    logging.info('Main Started at: ' + mTime[0])
    # logging.debug('log this too')
    domains, subdomains = get_domains_and_subdomains_from_aws()
    # get_subdomains_from_shodan_google(domains, subdomains)
    hijackable_subs = get_hijackable_subs(subdomains, num_of_threads=30)
    # end_points = check_available_endpoints(subdomains, num_of_threads=200)
    fetch_and_compare_old_data()
    write_to_files()

    mTime.append(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))
    logging.info('Main Finished at: ' + mTime[1])
    with open('mTime', 'w') as outFile:
        outFile.write(mTime[0] + '\n')
        outFile.write(mTime[1])
