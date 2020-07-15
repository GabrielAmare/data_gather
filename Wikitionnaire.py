import sys

import bs4

from .GathererTemplate import GathererTemplate


class Wikitionnaire(GathererTemplate):
    @classmethod
    def read_VER_CON(cls, result, word, element):
        data = [[
            cell.text.replace('\n', '')
            for i_col, cell in enumerate(row.select('td'))]
            for i_row, row in enumerate(element.select('tr'))]
        data = [[cell for cell in row if cell] for row in data]
        data = [row for row in data if row]
        data = [cell for row in data for cell in row]

        mood_table = {
            'Indicatif': 'IND',
            'Subjonctif': 'SUB',
            'Impératif': 'IMP',
            'Participe': 'PAR'
        }
        tense_table = {
            'Présent': 'PR',
            'Imparfait': 'IM',
            'Passé simple': 'PS',
            'Futur simple': 'FS',
            'Passé': 'PA'
        }

        def startswith(content, *items):
            for item in items:
                if content.startswith(item):
                    return item

        mood, tense = None, None
        for item in data:
            if item in mood_table:
                mood = mood_table[item]
            elif item in tense_table:
                tense = tense_table[item]
            else:
                if item.endswith(word):
                    entity = None
                    if startswith(item, 'je', "que je", "j'", "que j'", "j’", "que j’"):
                        entity = '1S'
                    elif startswith(item, 'tu', "que tu", "t'", "que t'"):
                        entity = '2S'
                    elif startswith(item, 'il/elle/on', "qu'il/elle/on", "qu’il/elle/on"):
                        entity = '3S'
                    elif startswith(item, '(masculin singulier)'):
                        entity = '3SM'
                    elif startswith(item, '(2e personne du singulier)'):
                        entity = '2S'
                    elif startswith(item, 'ils/elles', 'qu’ils/elles'):
                        entity = '3P'
                    if mood and tense and entity:
                        code = f'VER-CON-{mood}-{tense}-{entity}'
                        result.add(code)
                    # else:
                    #     print('#', word, mood, tense, item)
                else:
                    tense = None

    @classmethod
    def read_NOM_COM_gender(cls, word, element, gender, number):
        text = element.text
        if text.startswith(word):
            if 'féminin' in text and not 'masculin' in text:
                # if element.text.endswith('féminin\n'):
                gender = 'F'
            elif 'masculin' in text and not 'féminin' in text:
                # elif element.text.endswith('masculin\n'):
                gender = 'M'
            elif 'masculin' in text and 'féminin' in text:
                gender = ''

            if 'singulier' in text and not 'pluriel' in text:
                # if element.text.endswith('féminin\n'):
                number = 'S'
            elif 'pluriel' in text and not 'singulier' in text:
                # elif element.text.endswith('masculin\n'):
                number = 'P'
            elif 'pluriel' in text and 'singulier' in text:
                number = ''
        return gender, number

    @classmethod
    def read_subtitle(cls, result, element):
        typecode = None
        if element.text.startswith('Préposition'):
            result.add('PRE')
        elif element.text.startswith('Nom de famille'):
            result.add('NOM-PRO-3')
        elif element.text.startswith('Forme de verbe'):
            typecode = 'VER-CON'
        elif element.text.startswith('Nom commun'):
            typecode = 'NOM-COM'
        elif element.text.startswith('Nom propre'):
            typecode = 'NOM-PRO'
        elif element.text.startswith('Prénom'):
            typecode = 'NOM-PRO'
        elif element.text.startswith('Article défini'):
            typecode = 'ART-DEF'
        elif element.text.startswith('Article indéfini'):
            typecode = 'ART-IND'
        elif element.text.startswith('Forme d’article défini'):
            typecode = 'ART-DEF'
        elif element.text.startswith('Forme d’article indéfini'):
            typecode = 'ART-IND'
        elif element.text.startswith('Forme de nom commun'):
            typecode = 'NOM-COM'
        elif element.text.startswith('Forme d’adjectif'):
            typecode = 'ADJ-QUA'
        elif element.text.startswith('Adjectif possessif'):
            typecode = 'ADJ-POS'
        elif element.text.startswith('Interjection'):
            typecode = 'INT-STR'
        # IGNORED SECTION YET !
        elif element.text.startswith('Verbe'):
            pass
        elif element.text.startswith('Déterminant'):
            pass
        elif element.text.startswith('Pronom personnel'):
            pass  # typecode = 'PRO-PER'
        elif element.text.startswith('Pronom interrogatif'):
            pass  # typecode = 'PRO-INT'
        elif element.text.startswith('Pronom relatif'):
            pass  # typecode = 'PRO-REL'
        elif element.text.startswith('Pronom démonstratif'):
            pass  # typecode = 'PRO-DEM'
        elif element.text.startswith('Pronom'):
            pass
        elif element.text.startswith('Article'):
            pass
        elif element.text.startswith('Conjonction'):
            pass
        elif element.text.startswith('Adverbe interrogatif'):
            pass
        elif element.text.startswith('Adverbe'):
            pass
        elif element.text.startswith('Forme de pronom personnel'):
            pass  # typecode = 'PRO-PER'
        elif element.text.startswith('Forme de pronom'):
            pass
        elif element.text.startswith('Adjectif'):
            typecode = 'ADJ-QUA'
        elif element.text.startswith('Postposition'):
            pass
        # IGNORED SECTIONS NOT DEFINING WORDS
        elif element.text.startswith('Particule [modifier le wikicode]'):
            pass
        elif element.text == 'Anagrammes[modifier le wikicode]':
            pass
        elif element.text == 'Taux de reconnaissance[modifier le wikicode]':
            pass
        elif element.text == 'Étymologie[modifier le wikicode]':
            pass
        elif element.text == 'Prononciation[modifier le wikicode]':
            pass
        elif element.text == 'Voir aussi[modifier le wikicode]':
            pass
        elif element.text == 'Références[modifier le wikicode]':
            pass
        elif element.text == 'Lettre [modifier le wikicode]':
            pass
        elif element.text == 'Symbole [modifier le wikicode]':
            pass
        else:
            print(f"""        elif element.text.startswith({repr(element.text)}):
            pass""")

        return typecode

    @classmethod
    def parse_ADJ_QUA_table(cls, result, word, element):
        data = element.text.split('\n')
        data = map(str.strip, data)
        data = filter(len, data)
        data = list(data)
        formats = [
            (2, {0: 'Invariable'}, {1: 'ADJ-QUA-3'}),
            (4, {0: 'Masculin', 2: 'Féminin'}, {1: 'ADJ-QUA-3M', 3: 'ADJ-QUA-3F'}),
            (5, {0: 'Singulier', 1: 'Pluriel'}, {2: 'ADJ-QUA-3S', 3: 'ADJ-QUA-3P'}),
            (6, {0: 'Singulier', 1: 'Pluriel', 2: 'Masculinet féminin'}, {3: 'ADJ-QUA-3S', 4: 'ADJ-QUA-3P'}),
            (7, {0: 'Singulier', 1: 'Pluriel', 2: 'Masculin', 4: 'Féminin'}, {3: 'ADJ-QUA-3M', 5: 'ADJ-QUA-3SF', 6: 'ADJ-QUA-3PF'}),
            (8, {0: 'Singulier', 1: 'Pluriel', 2: 'Masculin', 5: 'Féminin'}, {3: 'ADJ-QUA-3SM', 4: 'ADJ-QUA-3PM', 6: 'ADJ-QUA-3SF', 7: 'ADJ-QUA-3PF'}),
        ]
        for L, X, Y in formats:
            if len(data) == L and all(data[key] == val for key, val in X.items()):
                for key, val in Y.items():
                    if data[key].startswith(word):
                        result.add(val)
                        break
                else:
                    continue
                break
        else:
            print('ADJ-QUA-3?? : table ->', word, data)

    @classmethod
    def scan(cls, word, document, result):
        firstHeading = document.select_one('#firstHeading')
        if firstHeading.text == word:
            lang = None
            typecode = None
            gender = None
            number = None
            for element in document.select('#bodyContent .mw-parser-output > *'):
                if not isinstance(element, bs4.NavigableString):
                    if element.name == 'h2':  # titre section
                        if element.text == 'Français[modifier le wikicode]':
                            lang = 'FR'
                        else:
                            lang = None
                    elif element.name == 'h3':  # titre secondaire
                        if lang == 'FR':
                            typecode = cls.read_subtitle(result, element)

                            # if typecode:
                            #     print(repr(word), repr(typecode))
                    elif element.name == 'table':
                        if lang == 'FR':
                            if typecode == 'VER-CON':
                                cls.read_VER_CON(result, word, element)
                            elif typecode == 'NOM-COM':
                                data = element.text.split('\n')
                                data = map(str.strip, data)
                                data = filter(len, data)
                                data = list(data)
                                if len(data) == 5 and data[0] == 'Singulier' and data[1] == 'Pluriel':
                                    number = 'S' if data[2] == word else 'P' if data[3] == word else '?'
                                elif len(data) == 2 and data[0] == 'Invariable':
                                    number = '' if data[1].startswith(word) else '?'
                                elif len(data) == 2 and data[0] == 'Singulier et pluriel':
                                    number = '' if data[1].startswith(word) else '?'
                                elif len(data) == 6 and data[0] == 'Singulier' and data[1] == 'Pluriel' and data[2] == 'Masculinet féminin':
                                    if data[4].startswith(word):
                                        result.add('NOM-COM-3P')
                                    elif data[3].startswith(word):
                                        result.add('NOM-COM-3P')
                                    else:
                                        print(f"NOM-COM-3?{gender if gender else '?'} : table ->", word, data)
                                else:
                                    print(f"NOM-COM-3?{gender if gender else '?'} : table ->", word, data)
                            elif typecode == 'ADJ-QUA':
                                cls.parse_ADJ_QUA_table(result, word, element)

                    elif element.name == 'p':  # text
                        if lang == 'FR':
                            if typecode == 'NOM-COM':
                                gender, number = cls.read_NOM_COM_gender(word, element, gender, number)
                                if number is not None and gender is not None:
                                    result.add(f'NOM-COM-3{number}{gender}')
                                else:
                                    print(f'-----> no gender ({gender}) or number ({number}) for {word}')
                            elif typecode == 'NOM-PRO':
                                gender, number = cls.read_NOM_COM_gender(word, element, gender, number)
                                if gender is not None:
                                    result.add(f'NOM-PRO-3{gender}')
                                else:
                                    print(f'-----> no gender ({gender}) for {word}')


                    elif element.name == 'ol':  # list
                        pass
                    elif element.name == 'h4':
                        pass
                    elif element.name == 'ul':
                        pass
                    elif element.name == 'h5':
                        pass
                    elif element.name == 'dl':
                        pass
                    elif element.name == 'div':
                        pass

        else:
            print(f"Wikitionnaire : {repr(word)} not found")

    #
    # @classmethod
    # def format_table(cls, table):
    #     return [d for a in table.text.split('\n') for b in a.split('\\') for c in b.split('(') for d in c.split(')') if
    #             d]
    #
    # @classmethod
    # def read_nom_commun(cls, result, word, document, link, anchor=None, logfile=None):
    #     ref = document.select_one(link) if anchor is None else anchor
    #     if ref:
    #         table = cls.next(ref.parent if anchor is None else anchor)
    #         data = [[
    #             cell.text.replace('\n', '')
    #             for i_col, cell in enumerate(row.select('td'))]
    #             for i_row, row in enumerate(table.select('tr'))]
    #         data = [[cell for cell in row if cell] for row in data]
    #         data = [row for row in data if row]
    #         data = [cell for row in data for cell in row]
    #         if len(data) == 3:
    #             singular, plural = data[0], data[1]
    #             p1 = table
    #             while not p1.name == 'p':
    #                 p1 = cls.next(p1)
    #             text = p1.text
    #             print(text)
    #             gender = 'M' if 'masculin' in text else 'F' if 'féminin' in text else '?'
    #             number = 'S' if singular == word else 'P' if plural == word else '?'
    #             result.add(f"NOM-COM-3{number}{gender}")
    #
    # @classmethod
    # def read_adjectif(cls, result, word, document, link, anchor=None, logfile=None):
    #     ref = document.select_one(link) if anchor is None else anchor
    #     if ref:
    #         table = cls.next(ref.parent if anchor is None else anchor)
    #         data = cls.format_table(table)
    #         # SM, SF, PM, PF = data[3], data[5], data[8], data[10]
    #         # code = {SM: 'SM', SF: 'SF', PM: 'PM', PF: 'PF'}.get(word, '??')
    #         # result.add(f'ADJ-QUA-3{code}')
    #     else:
    #         logfile.write(f'\nread_adjectif : invalid {ref.text}')
    #
    # @classmethod
    # def read_adverbe(cls, result, word, document, link, anchor=None, logfile=None):
    #     ref = document.select_one(link) if anchor is None else anchor
    #     if ref:
    #         table = cls.next(ref.parent if anchor is None else anchor)
    #         p1 = cls.next(table)
    #         p2 = cls.next(cls.next(table))
    #         text = p1.text + p2.text
    #         print('adverbe', repr(text))
    #
    # @classmethod
    # def read_verb(cls, result, word, document, link, anchor=None, logfile=None):
    #     ref = document.select_one(link) if anchor is None else anchor
    #     if ref:
    #         table = cls.next(ref.parent if anchor is None else anchor)
    #         data = [[
    #             cell.text.replace('\n', '')
    #             for i_col, cell in enumerate(row.select('td'))]
    #             for i_row, row in enumerate(table.select('tr'))]
    #         data = [[cell for cell in row if cell] for row in data]
    #         data = [row for row in data if row]
    #         data = [cell for row in data for cell in row]
    #
    #         mood_table = {
    #             'Indicatif': 'IND',
    #             'Subjonctif': 'SUB',
    #             'Impératif': 'IMP',
    #             'Participe': 'PAR'
    #         }
    #         tense_table = {
    #             'Présent': 'PR',
    #             'Imparfait': 'IM',
    #             'Passé simple': 'PS',
    #             'Futur simple': 'FS',
    #             'Passé': 'PA'
    #         }
    #
    #         def startswith(content, *items):
    #             for item in items:
    #                 if content.startswith(item):
    #                     return item
    #
    #         mood, tense = None, None
    #         for item in data:
    #             if item in mood_table:
    #                 mood = mood_table[item]
    #             elif item in tense_table:
    #                 tense = tense_table[item]
    #             else:
    #                 if item.endswith(word):
    #                     entity = None
    #                     if startswith(item, 'je', "que je", "j'", "que j'", "j’", "que j’"):
    #                         entity = '1S'
    #                     elif startswith(item, 'tu', "que tu", "t'", "que t'"):
    #                         entity = '2S'
    #                     elif startswith(item, 'il/elle/on', "qu'il/elle/on", "qu’il/elle/on"):
    #                         entity = '3S'
    #                     elif item.startswith('(masculin singulier)'):
    #                         entity = '3SM'
    #                     elif item.startswith('(2e personne du singulier)'):
    #                         entity = '2S'
    #                     if mood and tense and entity:
    #                         code = f'VER-CON-{mood}-{tense}-{entity}'
    #                         result.add(code)
    #                     else:
    #                         print('#', word, mood, tense, item)
    #                 else:
    #                     tense = None
    #     else:
    #         logfile.write(f'\nread_verb : invalid {ref.text}')
    #
    # @classmethod
    # def read_section(cls, result, word, document, section, anchor=None, logfile=None):
    #     link = section.attrs.get('href')
    #
    #     if "Pronom personnel" in section.text:
    #         logfile.write(f'\nFOUND : Pronom personnel')
    #         cls.read_pronom_personnel(result, word, document, link, anchor, logfile=logfile)
    #     elif 'Nom commun' in section.text:
    #         logfile.write(f'\nFOUND : Nom Commun')
    #         cls.read_nom_commun(result, word, document, link, anchor, logfile=logfile)
    #     elif 'Adjectif' in section.text:
    #         logfile.write(f'\nFOUND : Adjectif')
    #         cls.read_adjectif(result, word, document, link, anchor, logfile=logfile)
    #     elif 'Adverbe' in section.text:
    #         logfile.write(f'\nFOUND : Adverbe')
    #         cls.read_adverbe(result, word, document, link, anchor, logfile=logfile)
    #     elif 'Forme de verbe' in section.text:
    #         logfile.write(f'\nFOUND : Verbe Conjugué')
    #         cls.read_verb(result, word, document, link, anchor, logfile=logfile)
    #     elif 'Préposition' in section.text:
    #         logfile.write(f'\nFOUND : Préposition')
    #         result.add('PRE')
    #     else:
    #         logfile.write(f'\nread_section : unrecognized {section.text}')
    #
    # @classmethod
    # def read_lang(cls, result, word, document, lang, logfile=None):
    #     nextto = cls.next(lang)
    #     if nextto is not None:
    #         for section in nextto.select('li > a'):
    #             if section.parent.parent.parent == lang.parent:
    #                 cls.read_section(result, word, document, section, logfile=logfile)
    #     else:
    #         logfile.write(f'\nread_lang : invalid nextto {lang.text}')

    @classmethod
    def getset(cls, word: str) -> set:
        result = set()
        with open('log.txt', mode='a', encoding='utf-8') as logfile:
            document = cls.get_html(f"https://fr.wiktionary.org/wiki/{word}")

            if document:
                cls.scan(word, document, result)

                # summary = document.select_one("#toc")
                # if summary:
                #     for lang in document.select("#toc > ul > li > a"):
                #         if lang.text.endswith('Français'):
                #             cls.read_lang(result, word, document, lang, logfile=logfile)
                #         elif lang.text.endswith('Anglais'):
                #             pass
                # else:
                #     for section in document.select("h3"):
                #         if not section.text.startswith('\n'):
                #             cls.read_section(result, word, document, section, section, logfile=logfile)
        return result
