import configparser
import os
import config_parser

configfile = config_parser.configfile
configparser = configparser.ConfigParser(delimiters='=')


def main():
    config_parser.checkconfigfile()
    result = 0
    menu = {'1': "read_file", '2': "modify_file"}
    while True:
        result = create_menu(menu)
        # run the function defined
        possibles = globals().copy()
        possibles.update(locals())
        # func = possibles.get(menu[str(result)])
        func = possibles.get(result)
        if not func:
            raise NotImplementedError("Function %s not implemented" % menu[str(result)])
        func()


def create_menu(dictitems, prompt="Please Select:"):
    if type(dictitems) == list:
        if type(dictitems[0]) is tuple:
            dictitems = {str(i + 1): dictitems[i] for i in range(0, len(dictitems))}
        else:
            dictitems = {str(i + 1): dictitems[i] for i in range(0, len(dictitems))}
    dictitems.update({'0': 'exit'})
    while True:
        options = dictitems.keys()
        for entry in options:
            print(entry + ": " + str(dictitems[entry]))
        selection = input(prompt)
        if selection == '':
            clear_screen()
            print('please select a valid option')
        elif selection == '0':
            exit()
        elif int(selection) in range(1, len(dictitems)):
            return dictitems[selection]
        else:
            clear_screen()
            print('please select a valid option')


def list_items(dictitems):
    if type(dictitems) == list:
        dictitems = {dictitems[i][0]: dictitems[i][1] for i in range(0, len(dictitems))}
    count = dictitems.keys()
    for i in count:
        print(i + " = " + dictitems[i])
    return


def read_file():
    clear_screen()
    print("select the section to display")
    section = get_sections()
    selected_section = create_menu(section)
    retval = print_section(selected_section)
    clear_screen()
    # return create_menu(get_values(retval))
    list_items(retval)
    print()


def modify_file():
    clear_screen()
    print("select the section to modify")
    section = get_sections()
    selected_section = create_menu(section)
    retval = print_section(selected_section)
    clear_screen()
    actions = ['add', 'edit', 'remove']
    action = create_menu(actions, "Select the action to perform:")
    clear_screen()

    def get_option():
        clear_screen()
        option = create_menu(retval)
        return option

    if action == "add":
        new_key = input("Enter name of the key to add: ")
        new_value = input("Enter path of the directory or file to add: ")
        configparser.set(selected_section, new_key, new_value)
    elif action == "remove":
        option = get_option()
        print("removing value " + option[0])
        configparser.remove_option(selected_section, option[0])
    elif action == "edit":
        option = get_option()
        new_val = input('What is the new value: ')
        configparser.set(selected_section, option[0], new_val)
    with open(configfile, 'w') as cf:
        configparser.write(cf)
    exit()


def get_keys(itemlist):
    ret = []
    for i in itemlist:
        ret.append(i[0])
    return ret


def get_values(itemlist):
    ret = []
    for i in itemlist:
        ret.append(i[1])
    return ret


def get_sections():
    configparser.read_file(open(configfile))
    return configparser.sections()


def print_section(selected_section):
    # clear_screen()
    values = []
    with open(configfile) as cf:
        for f in configparser.items(selected_section):
            values.append(f)
            # values.append(f[1])
    # SET TO VALUES.APPEND(F) for key and value to be returned
    return values


def exit():
    raise SystemExit


def clear_screen():
    os.system('cls')


if __name__ == '__main__':
    main()
