import csv
import operator
import re

import Stemmer
import matplotlib.pyplot as plt
import stop_words

OUTPUT_FOLDER = 'output1/'

stop_words_en = stop_words.get_stop_words('en')
stemmer = Stemmer.Stemmer('english')
global number_of_words_spam
global number_of_words_ham

number_of_words_spam = 0
number_of_words_ham = 0

# Функция построения графика(Использует библиотелку matplotlib)
def build_plot(content, file_name):
    i = 0
    words_list = list()
    nums = list()
    for k, v in content:
        if i == 13:
            break
        words_list.append(k)
        nums.append(v)
        i += 1
    plt.plot(words_list, nums, linewidth=2.0)
    plt.savefig(OUTPUT_FOLDER + file_name)
    print("График построен получется да ну да а што")
    plt.show()
    

# Функция схранения данных в файл
def save_to_file(file_name, content):
    with open(OUTPUT_FOLDER + file_name, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['word'] + ['number'])
        for key, value in content:
            writer.writerow([key] + [str(value)])
    file.close()

# Функция добавления слов в словарь
def add_to_dict(dict_element, words_to_add, word_length):
    global number_of_words_spam
    for word in words_to_add:
        word = word.lower()
        if word in stop_words_en or len(word) < 2:
            continue
        num = dict_element.get(word)
        if not num:
            dict_element[word] = 1
        else:
            dict_element[word] = num + 1
        add_to_length_dict(word, word_length)

# Функция установки размера словаря
def add_to_length_dict(word, length_dict):
    len_num = length_dict.get(len(word))
    if not len_num:
        length_dict[len(word)] = 1
    else:
        length_dict[len(word)] = len_num + 1

# Функция чтения данных из файла
def read_from_file(ham_dict, spam_dict, word_length_ham, word_length_spam, sentence_length_spam, sentence_length_ham):
    global number_of_words_spam
    global number_of_words_ham
    with open("sms-spam-corpus.csv") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            sentence = stemmer.stemWord(row['v2'])
            words = re.findall('[a-zA-Z]+', sentence)
            if row['v1'] == 'spam':
                number_of_words_spam += len(words)
                add_to_length_dict(sentence, sentence_length_spam)
                add_to_dict(spam_dict, words, word_length_spam)
            elif row['v1'] == 'ham':
                number_of_words_ham += len(words)
                add_to_length_dict(sentence, sentence_length_ham)
                add_to_dict(ham_dict, words, word_length_ham)
    csv_file.close()


def build_word_length_plot(spam_lengths, ham_lengths):
    create_sub_curve(spam_lengths, 'spam', 'word_length_mean.txt')
    create_sub_curve(ham_lengths, 'ham', 'word_length_mean.txt')
    plt.xlabel('words length')
    plt.ylabel('Frequency')
    plt.legend()
    plt.savefig(OUTPUT_FOLDER + "words_frequency.png")
    plt.show()


def build_sentence_length_plot(spam_lengths, ham_lengths):
    create_sub_curve(spam_lengths, 'spam', 'sentence_length_mean.txt')
    create_sub_curve(ham_lengths, 'ham', 'sentence_length_mean.txt')
    plt.xlabel('sentence length')
    plt.ylabel('Frequency')
    plt.legend()
    plt.savefig(OUTPUT_FOLDER + "sentence_frequency.png")
    plt.show()


def create_sub_curve(lengths, sub_curve_name, mean_file_name):
    x = list()
    y = list()
    quantity = 0
    sum_for_median = 0
    for key, value in lengths:
        quantity += value
        sum_for_median += key * value
        x.append(key)
        y.append(value)
    mean = sum_for_median / quantity
    with open(OUTPUT_FOLDER + mean_file_name, 'a+') as file:
        file.writelines(['mean for ', str(sub_curve_name), ':', str(mean), '\n'])
    file.close()
    plt.plot(x, y, label=sub_curve_name)


def clear_file(file_name):
    f = open(file_name, "w")
    f.close()


def main():
    global number_of_words_spam
    global number_of_words_ham
    clear_file(OUTPUT_FOLDER + 'sentence_length_mean.txt')
    clear_file(OUTPUT_FOLDER + 'word_length_mean.txt')
    spam_dict = dict()
    ham_dict = dict()
    word_length_spam = dict()
    word_length_ham = dict()
    sentence_length_spam = dict()
    sentence_length_ham = dict()

    read_from_file(ham_dict, spam_dict, word_length_ham, word_length_spam, sentence_length_spam, sentence_length_ham)
    for key, value in word_length_spam.items():
        num = word_length_spam[key]
        word_length_spam[key] = num / number_of_words_spam
    for key, value in word_length_ham.items():
        num = word_length_ham[key]
        word_length_ham[key] = num / number_of_words_ham
    spam_dict = sorted(spam_dict.items(), key=operator.itemgetter(1), reverse=True)
    ham_dict = sorted(ham_dict.items(), key=operator.itemgetter(1), reverse=True)
    word_length_spam = sorted(word_length_spam.items(), key=operator.itemgetter(0), reverse=True)
    word_length_ham = sorted(word_length_ham.items(), key=operator.itemgetter(0), reverse=True)
    sentence_length_spam = sorted(sentence_length_spam.items(), key=operator.itemgetter(0), reverse=True)
    sentence_length_ham = sorted(sentence_length_ham.items(), key=operator.itemgetter(0), reverse=True)

    save_to_file('spam.csv', spam_dict)
    save_to_file('ham.csv', ham_dict)

    build_plot(spam_dict, 'spam.png')
    build_plot(ham_dict, 'ham.png')
    build_word_length_plot(word_length_spam, word_length_ham)
    build_sentence_length_plot(sentence_length_spam, sentence_length_ham)


main()
