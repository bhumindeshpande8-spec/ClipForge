# backend/chat.py

def apply_chat_command(edit_plan, message):
    """
    Parse simple commands like:
    "Make captions bolder"
    "Remove animation"
    """
    msg = message.lower()

    if "bolder" in msg:
        for e in edit_plan:
            e["fontsize"] = 40  # override
    if "remove animation" in msg:
        for e in edit_plan:
            e["animation"] = "none"
    return edit_plan
