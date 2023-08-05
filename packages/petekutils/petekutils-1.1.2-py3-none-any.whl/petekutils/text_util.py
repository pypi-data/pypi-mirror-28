class TextUtil(object):
    """docstring for TextUtil."""
    def __init__(self):
        super(TextUtil, self).__init__()

    @staticmethod
    def text_lower(text):
        turkish_chars = [("Ü", "ü"), ("Ö", "ö"), ("İ", "i"), ("Ş", "ş"),
        ("Ç", "ç"), ("Ğ", "ğ"), ("I", "ı")]
        ret_text = text
        for t in turkish_chars:
            ret_text = ret_text.replace(t[0], t[1])
        return ret_text.lower()

    @staticmethod
    def get_clean_text(obj, keywords):
        """ get len of obj """
        #res = hlp.get_binary_image(obj["$oid"])
        data = "<html><body>%s</body></html>" % obj
        rettext = pq(data).text()[:250]
        for k in keywords:
            rettext = self.text_lower(rettext).replace(k, "<span style='background-color: #D7E9FA;'>" + k + "</span>")
        return rettext + " ..."

    @staticmethod
    def text_upper(text):
        return text.upper()
