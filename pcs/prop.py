import sys
import usage
import utils
import xml.dom.minidom
from xml.dom.minidom import parseString

def property_cmd(argv):
    if len(argv) == 0:
        argv = ["list"]

    sub_cmd = argv.pop(0)
    if (sub_cmd == "help"):
        usage.property()
    elif (sub_cmd == "set"):
        set_property(argv)
    elif (sub_cmd == "list" or sub_cmd == "show"):
        list_property(argv)
    else:
        usage.property()
        sys.exit(1)

def set_property(argv):
    for arg in argv:
        args = arg.split('=')
        if (len(args) != 2):
            print "Invalid Property: " + arg
            continue
        utils.set_cib_property(args[0],args[1])

def list_property(argv):
    print_all = False
    if len(argv) == 0:
        print_all = True

    (output, retVal) = utils.run(["cibadmin","-Q","--scope", "crm_config"])
    if retVal != 0:
        print "ERROR: Unable to get crm_config"
        print output
        exit(1)
    dom = parseString(output)
    de = dom.documentElement
    properties = de.getElementsByTagName("nvpair")
    for prop in properties:
        if print_all == True or (argv[0] == prop.getAttribute("name")):
            print prop.getAttribute("name") + ": " + prop.getAttribute("value")
