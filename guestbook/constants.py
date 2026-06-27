from django.templatetags.static import static

# used for authoring entries w/ clickable smilies
SMILIES = [
    {"emoticon": ":)", "url": static("images/smilies/smile.gif"), "alt": "Smile"},
    {"emoticon": ":-)", "url": static("images/smilies/lol.gif"), "alt": "LOL"},
    {"emoticon": ";)", "url": static("images/smilies/wink.gif"), "alt": "winkywinky"},
    {"emoticon": ":(", "url": static("images/smilies/frown.gif"), "alt": "frown"},
    {"emoticon": ":y)", "url": static("images/smilies/crying.gif"), "alt": "crying"},
    {
        "emoticon": ":]",
        "url": static("images/smilies/biggrin.gif"),
        "alt": "big smile",
    },
    {
        "emoticon": ":?)",
        "url": static("images/smilies/confused.gif"),
        "alt": "confused",
    },
    {"emoticon": ":c)", "url": static("images/smilies/cool.gif"), "alt": "cool"},
    {"emoticon": ":e)", "url": static("images/smilies/eek.gif"), "alt": "eek"},
    {"emoticon": ":g)", "url": static("images/smilies/girl.gif"), "alt": "girl"},
    {
        "emoticon": ":r)",
        "url": static("images/smilies/redface.gif"),
        "alt": "redface",
    },
    {
        "emoticon": ":8)",
        "url": static("images/smilies/rolleyes.gif"),
        "alt": "roll eyes",
    },
    {"emoticon": ":}", "url": static("images/smilies/tongue.gif"), "alt": "tongue"},
    {"emoticon": ":i)", "url": static("images/smilies/idea.gif"), "alt": "idea"},
    {"emoticon": ":pi", "url": static("images/smilies/pimp.gif"), "alt": "pimp"},
    {"emoticon": ":up", "url": static("images/smilies/up.gif"), "alt": "up"},
    {"emoticon": ":do", "url": static("images/smilies/down.gif"), "alt": "down"},
    {"emoticon": ":ty", "url": static("images/smilies/type.gif"), "alt": "typing"},
    {
        "emoticon": ":gr",
        "url": static("images/smilies/dance1.gif"),
        "alt": "dancingstick",
    },
]

# for replacing :) -> img tag
SMILIES_MAP = {item["emoticon"]: item["url"] for item in SMILIES}
