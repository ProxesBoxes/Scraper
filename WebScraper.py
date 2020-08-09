#!/usr/bin/python3
import requests
import string
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self, required_tag, required_value):
        HTMLParser.__init__(self)
        self.required_tag = required_tag
        self.required_value = required_value
        self.recording = 0
        self.data = []

    def handle_starttag(self, tag, attrs):
        if tag == self.required_tag:
            for name, value in attrs:
                if value == self.required_value:
                    self.recording = 1

    def handle_endtag(self, tag):
        if tag == self.required_tag and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if self.recording:
            self.data.append(data)


base_url = 'https://www.SlangSite.com/slang/'
end_url = '.html'
# Array to hold all of the words
words = []

# Loop through the letters of the alphabet
for letter in string.ascii_uppercase:
    # Something, something, the word your looking for is pagination
    page = 1

    url_req = requests.get(f'{base_url}{letter}{end_url}')
    # Read out the div tags that contains the words
    columnist_parse = MyHTMLParser('font', '3')
    columnist_parse.feed(url_req.text)
    # Loop through the words and make sure they actually exist, add them to array
    for columnist in columnist_parse.data:
        if columnist != '\n' and len(columnist) >= 1:
            words.append(columnist)
    columnist_parse.close()

print("number of words: " + str(len(words)))

unique_words = list(set(words))

print("number of unique words: " + str(len(unique_words)))

# Create a file and write all of the words to it
word_list = open ("SlangSite.txt", "w")
for word in words:
    word_list.write(word[:-2] + '\n')
word_list.close()

word_list = open ("SlangSiteUnique.txt", "w")
for word in unique_words:
    word_list.write(word[:-2] + '\n')
word_list.close()
