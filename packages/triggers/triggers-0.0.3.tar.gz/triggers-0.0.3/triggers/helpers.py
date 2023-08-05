from pydoc import locate

def trigger(trigger_name, *args):
    try:
        from config import triggers as trigger_list
    except ImportError:
        raise Exception(
            '\033[95mNo trigger configuration found in `config/triggers.py`. Try running `craft publish triggers`\033[0m')

    # if trigger_name contains an @ symbol then execute a different function
    if '@' in trigger_name:
        trigger_split = trigger_name.split('@')
        action = locate(trigger_list.TRIGGERS[trigger_split[0]])()
        getattr(action, trigger_split[1])(*args)
    else:
        locate(trigger_list.TRIGGERS[trigger_name])().action()
