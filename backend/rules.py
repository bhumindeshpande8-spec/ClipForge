# backend/rules.py

def apply_rules(segments):
    """
    Decide captions, animations, and styles
    """
    edits = []

    for i, seg in enumerate(segments):
        edit = {
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"],
            "style": "caption",
            "animation": "fade"
        }

        if i == 0:
            edit["style"] = "title"

        if len(seg["text"].split()) > 8:
            edit["animation"] = "pop"

        edits.append(edit)

    return edits