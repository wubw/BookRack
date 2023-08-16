import os

def check_folder(reading_status):
    folder =  '../data/' + reading_status
    csv_f = open('../data/' + reading_status + '.csv', "r", encoding='utf_8_sig')
    csv_d = csv_f.read()
    csv_f.close()
    for f in os.listdir(folder):
        book_url = 'https://book.douban.com/subject/' + f[:len(f)-len('.html')]
        if book_url in csv_d:
            continue
        print(book_url)

#check_folder('reading')
#check_folder('have_read')
check_folder('will_read')
