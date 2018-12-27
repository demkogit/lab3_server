from xmlrpc.server import SimpleXMLRPCServer
import urllib.request
from bs4 import BeautifulSoup

server = SimpleXMLRPCServer(('localhost', 9000), logRequests=True)
server.register_introspection_functions()
server.register_multicall_functions()
sym = '?!(),./\\|@#$%^&*:;\''


def del_sym(text):
    for s in sym:
        text = text.replace(s, ' ')
    return text


class WordService:

    def countOneWord(self, text, word):
        count = 0
        text = del_sym(text)
        for w in text.split():
            if (w == word):
                count += 1
        return count

    def countCharacters(self, text):
        d = {}
        for s in text:
            if not d.get(s):
                d[s] = 1
            else:
                d[s] += 1
        return d

    def countWords(self, text):
        d = {}
        text = del_sym(text)
        for w in text.split():
            if not d.get(w):
                d[w] = 1
            else:
                d[w] += 1
        return d

    def makeCaps(self, text):
        return text.upper()

    def countWordsOnWebPage(self, url):
        try:
            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html, features="lxml")

            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text()

            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
        except Exception:
            return 'ERROR!'

        return self.countWords(text)


server.register_instance(WordService())

server.serve_forever()
