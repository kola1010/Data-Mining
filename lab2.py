import csv
import re

import Stemmer

stemmer = Stemmer.Stemmer('english')
global overall_ham, overall_spam


def read_data(file_path):
    map_words = dict()
    with open(file_path) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            map_words[row['word']] = int(row['number'])
    csv_file.close()
    return map_words


def find_number_of_words_in_dict(word, words_dict):
    for key in words_dict:
        if key == word:
            return words_dict[key]

    return 0


def main():
    global overall_ham, overall_spam
    overall_spam = 0
    overall_ham = 0
    print('enter message:')
    sentence = input()
    words = re.findall('[a-zA-Z]+', sentence)
    ham_dict = read_data('output1/ham.csv')
    for key in ham_dict:
        overall_ham += ham_dict[key]
    spam_dict = read_data('output1/spam.csv')
    for key in spam_dict:
        overall_spam += spam_dict[key]
    spam_probability = 1
    ham_probability = 1
    for word in words:
        word = stemmer.stemWord(word)
        num_in_ham = find_number_of_words_in_dict(word, ham_dict)
        num_in_spam = find_number_of_words_in_dict(word, spam_dict)
        if num_in_ham == 0:
            overall_ham += 1
        if num_in_spam == 0:
            overall_spam += 1
        spam_probability *= (num_in_spam + 1) / overall_spam
        ham_probability *= (num_in_ham + 1) / overall_ham

    if spam_probability > ham_probability:
        print('spam')
        print(spam_probability)
    else:
        print('ham')
        print(ham_probability)


main()
