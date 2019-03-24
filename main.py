from html.parser import HTMLParser
import urllib.request
import datetime
import time
import sys


class MyParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.song = Song()  # (time, artist, title)
        self.previous_song = Song()
        self.artistBool = False
        self.songBool = False
        self.flag = False

    @staticmethod
    def if_song(attrs, what):
        for (i, j) in attrs:
            if i == "id" and j == what+"0":
                return True
        return False

    def handle_starttag(self, tag, attrs):
        if tag == "span":
            if self.if_song(attrs, "artist"):
                self.artistBool = True
            elif self.if_song(attrs, "title"):
                self.songBool = True

    def handle_data(self, data):
        if self.artistBool:
            if self.flag:
                self.song.name = data
                self.flag = False
            self.artistBool = False
        if self.songBool:
            if self.previous_song.title != data:
                self.song.title = data
                self.flag = True
            self.songBool = False
        if self.song != self.previous_song and self.song.title != "" and self.song.name != "":
            self.previous_song = self.song
            self.song.time = '{0:%H:%M}'.format(datetime.datetime.now())
            self.write_to_file()

    def format(self):
        print(str(self.song))

    def feed(self, data):
        super().feed(data)

    def write_to_file(self):
        with open('save/{0:%Y-%m-%d}'.format(datetime.datetime.now()), 'a') as f:
            f.write(str(self.song))
            self.song = Song()

    def error(self, message):
        super().error(message)


class Song:
    def __init__(self):
        self.title = ""
        self.name = ""
        self.time = ""

    def __eq__(self, other) -> bool:
        return self.title == other.title and self.name == other.name

    def __repr__(self) -> str:
        return "{:10}{:30}{:30}\n".format(self.time, self.name, self.title)


def main():
    url = "http://apps.streamlicensing.com/covers_widget.cgi?sid=3382&output=5&orientation=vertical&seed=965766"
    html_parser = MyParser()
    while True:
        try:
            url_html = urllib.request.urlopen(url).read()
            html_parser.feed(str(url_html))
        except urllib.error.URLError as err:
            print("[-] Brak połączenia z internetem", file=sys.stderr)
        except Exception as err:
            print("[-] Nieznany błąd", file=sys.stderr)
            print(err, file=sys.stderr)
        time.sleep(60)


if __name__ == "__main__":
    main()
