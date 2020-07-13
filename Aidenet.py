from data_gather.GathererTemplate import GathererTemplate


class Aidenet(GathererTemplate):
    @classmethod
    def adverbes(cls):
        url = "http://www.aidenet.eu/grammaire20a.htm"
        document = cls.get_html(url)
        selector = ".main > p"

        for parag in document.select(selector):
            text = parag.text

            textmap = {
                "de temps et d'aspect": ["TEM", "ASP"],
                "de lieu": ["LIE"],
                "d'affirmation ou de doute": [],
                "de négation": [],
            }

            if 'Adverbes' in text:
                index = text.index('Adverbes')

                codes = []
                for key, alt in textmap.items():
                    if key in text:
                        codes = alt

                # print(text[index+8:].replace('*', ''))
                table = cls.next(parag)
                if not (table and table.name == 'table'):
                    table = cls.next(table)

                if table and table.name == 'table':
                    data = table.text.split('\n')
                    data = filter(len, data)
                    data = [e.replace('-', ' ').replace('*', '').replace('?', '').replace("'", '').strip() for e in data]
                    for code in codes:
                        for word in data:
                            yield word, f"ADV-{code}"



