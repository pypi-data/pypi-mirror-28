import cfscrape
import argparse
import sys
import time
import thread
import re
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
def notify_single(url, attacker, team, timeout):
    global post_url
    params = {'attacker': attacker, 'team': team, 'poc': 'SQL Injection', 'url': url}
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    try:
        notify_request = scraper.post(
                                        post_url,
                                        timeout=timeout,
                                        data=params,
                                        headers=headers
                                    )
    except Exception as e:
        raise Exception(str(e))
    else:
        if notify_request.status_code != 200:
            raise Exception("{} {}".format(notify_request.status_code, notify_request.reason))
        result = re.findall(r"\">(.*)<span", notify_request.text, re.M|re.I)[0] #re.sub("<.*?>", "", notify_request.text.lower())
        if "sukses" in notify_request.text.lower():
            return [True, result]
        else:
            return [False, result]
def status(icon,message, x=False, additional_escape=False):
    now = time.strftime("%H:%M:%S")
    if x == False:
        x = ""
    else:
        x = " "
    if icon == "!":
        escape = color.REVERSE+color.FAIL
    else:
        escape = color.OKGREEN
    if additional_escape != False:
        escape = str(additional_escape)
    print escape+color.BOLD+'[' + icon + ']'+ color.ENDC + escape + "[{}]".format(now) + x + message + color.ENDC
def wrapsbrace(text, x=False):
    if x == False:
        x = ""
    else:
        x = " "
    return "[{}]{}".format(text, x)

def main():
    print color.BOLD+color.WARNING+"+-+-+-+-+-+-+-+-+"+color.ENDC+color.BOLD+" Defacer.ID Mass Notifier"+color.ENDC
    print color.BOLD+color.WARNING+"|n|0|t|i|f|i|e|r|"+color.ENDC+color.BOLD+" Author: P4kL0nc4t"+color.ENDC
    print color.BOLD+color.WARNING+"+-+-+-+-+-+-+-+-+"+color.ENDC+color.BOLD+" "+color.UNDERLINE+"https://github.com/p4kl0nc4t\n"+color.ENDC
    parser = argparse.ArgumentParser(prog='defid_notifier', description="defid_notifier is a tool used to notify a lot of defacement at once (mass) to Defacer.ID (https://defacer.id/).", epilog='If you had stuck, you can mail me at p4kl0nc4t@obsidiancyberteam.id')
    parser.add_argument('file', metavar='websites_list', help='path to websites list')
    parser.add_argument('attacker', metavar='nick', help='nick to be notified')
    parser.add_argument('team', metavar='team', help='team to be notified')
    parser.add_argument('--filter', action='store_true', help='show only successful notification')
    parser.add_argument('--verbose', action='store_true', help='increase the verbosity (include response from server)')
    parser.add_argument('--timeout', type=int, help='set how long client waits for response (default: 60)')
    parser.add_argument('--start-at', dest="startat", type=int, help='set notifier\'s start point (line number)')
    parser.add_argument('--end-when', dest="endwhen", type=int, help='set maximum website to be notified from the start point')
    parser.add_argument('--turbo', action='store_true', help='use TURBO mode, this mode uses same number of thread as the number of website in websites list. Warning! TURBO mode will consume a lot of memory depending on number of threads. It is recommended to just set website limit.')
    args = parser.parse_args()
    def pretty_notify_single(url):
        done = False
        while done == False:
            try:
                if args.timeout: timeout = int(args.timeout)
                else: timeout = 60
                notify = notify_single(url, args.attacker, args.team, timeout)
            except Exception as e:
                if not args.filter:
                    status("!", "exception: {}, sleeping 10s . . .".format(str(e)), True)
                time.sleep(10)
            else:
                done = True
                if notify[0] == True:
                    if args.verbose: status("*", "success: {} (resp: {})".format(url, str(notify[1])), True)    
                    else: status("*", "success: {}".format(url), True)
                else:
                    if not args.filter:
                        if args.verbose: status("!", "failed: {} (resp: {})".format(url, str(notify[1])), True)
                        else: status("!", "failed: {}".format(url), True)
                if args.turbo:
                    thread.exit()
    try:
        web_list = open(args.file, 'r').readlines()
    except Exception as e:
        status("!", "exception: {}, exiting . . .".format(str(e)), True)
        sys.exit()
    else:
        if args.startat:
            status("*", "user-config: starting count from line {}".format(str(args.startat)), True)
            if args.startat > len(web_list):
                status("!", "error! start_at should not greater than urls in websites list, exiting . . .", True)
                sys.exit()
            try: 
                web_list = web_list[-1*len(web_list)+args.startat-1:]
            except Exception as e:
                status("!", "exception: {}, sleeping 10s . . .".format(str(e)), True)
        status("*", "retreived {} urls from {}".format(len(web_list), args.file), True)
        if args.turbo: 
            status("!", "TURBO mode is enabled! {} threads will be created".format(len(web_list)), True, color.WARNING)
        iters = 1
        for url in web_list:
            url = url.strip()
            if args.turbo:
                thread.start_new_thread(pretty_notify_single, (url,))
            else:
                pretty_notify_single(url)
            if args.endwhen:
                if iters == args.endwhen:
                    status("*", "reached website limit (user setting), breaking . . .", True)
                    break
            iters += 1
        if args.turbo:
            while True: 
                pass
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write("\r")
        status("!", "ctrl+c detected, exiting . . .", True)
        sys.exit()