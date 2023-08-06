import cfscrape
import argparse
import sys
import time
post_url = "https://defacer.id/archives/notify"
scraper = cfscrape.create_scraper()
parser = argparse.ArgumentParser(prog='Spammer', description="Spammer is a tool used to send Grab Activation Code (SMS) to a phone number repeatedly. Spammer uses Grab's passenger API.", epilog='If you had stuck, you can mail me at p4kl0nc4t@obsidiancyberteam.id')
parser.add_argument('file', metavar='website_list', help='path to websites list')
parser.add_argument('nick', metavar='nick', help='nick to be notified')
parser.add_argument('team', metavar='team', help='team to be notified')
parser.add_argument('--filter', action='store_true', help='show only successful notification')
parser.add_argument('--timeout', type=int, help='set how long client waits for response (default: 60)')
args = parser.parse_args()
def notify_single(url, attacker, team):
    global post_url
    params = {'attacker': 'attacker', 'team': team, 'poc': 'SQL Injection', 'url': url}
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    try:
        notify_request = scraper.post(
                                        post_url,
                                        data=params,
                                        headers=headers
                                    )
    except Exception as e:
        raise Exception(str(e))
    else:
        if "sukses" in notify_request.text:
            return True
        else:
            return False
def status(icon,message, x=False):
    if x == False:
        x = ""
    else:
        x = " "
    print "[{}]{}{}".format(icon,x,message)
def wrapsbrace(text, x=False):
    if x == False:
        x = ""
    else:
        x = " "
    return "[{}]{}".format(text, x)
try:
    web_list = open(args.file, 'r')
except Exception as e:
    print status("!", "exception: {}, exiting . . .".format(str(e)), True)
    sys.exit()
else:
    for url in web_list.readlines():
        try:
            notify = notify_single(url, args.attacker, args.team)
        except Exception as e:
            if not args.filter:
                status("!", "exception: {}, sleeping 10s . . .".format(str(e)), True)
            time.sleep(10)
        else:
            if notify == True:
                status("*", "success: {}".format(url), True)
            else:
                if not args.filter:
                    status("!", "failed: {}".format(url), True)