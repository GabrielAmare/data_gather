from data_gather.GathererTemplate import GathererTemplate


class Wikipedia(GathererTemplate):
    @classmethod
    def random(cls, max=10):
        url = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"

        document = cls.get_html(url)

        count = 0
        for p in document.select('p'):
            text = p.text.replace('\n', ' ')
            text = text.strip()
            if text:
                count += 1
                yield text
                if count >= max:
                    break
