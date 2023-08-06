import cfscrape
import argparse
import sys
import time
class color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    REVERSE = '\033[7m'
post_url = "https://defacer.id/archives/notify"
scraper = cfscrape.create_scraper()
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

def main():
    print color.BOLD+color.WARNING+"+-+-+-+-+-+-+-+-+"+color.ENDC+color.BOLD+" Defacer.ID Mass Notifier"
    print color.BOLD+color.WARNING+"|n|0|t|i|f|i|e|r|"+color.ENDC+color.BOLD+" Author: P4kL0nc4t"
    print color.BOLD+color.WARNING+"+-+-+-+-+-+-+-+-+"+color.ENDC+color.BOLD+" "+color.UNDERLINE+"https://github.com/p4kl0nc4t\n"
    parser = argparse.ArgumentParser(prog='defid_notifier', description="defid_notifier is a tool used to notify a lot of defacement at once (mass) to Defacer.ID (https://defacer.id/).", epilog='If you had stuck, you can mail me at p4kl0nc4t@obsidiancyberteam.id')
    parser.add_argument('file', metavar='website_list', help='path to websites list')
    parser.add_argument('nick', metavar='nick', help='nick to be notified')
    parser.add_argument('team', metavar='team', help='team to be notified')
    parser.add_argument('--filter', action='store_true', help='show only successful notification')
    parser.add_argument('--timeout', type=int, help='set how long client waits for response (default: 60)')
    args = parser.parse_args()
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
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        status("!", "ctrl+c detected, exiting . . .", True)
        sys.exit()