import time
import random
from datetime import datetime
import os


def create_history_file():
    history_file = "history.txt"
    if not os.path.exists(path=history_file):
        print("WARNING. History file does not exist!")
        print("Creating a history file.")
        with open(file=history_file, mode="w") as hf:
            hf.close()


def save_history(session, generated_sent, answer, time_taken, accuracy):
    with open(file="history.txt", mode="a+") as file:
        file.write(
            f"Session {session},"
            f"Generated sentence {generated_sent},"
            f"Answer {answer},"
            f"Time taken {time_taken},"
            f"Accuracy {accuracy},"
            f"Save date {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
        )


def get_random_sentence(number_of_sentences):
    gen_sent_list = []
    with open(file="sentences.txt", mode="r") as file:
        sentences = file.read().splitlines()

        while len(gen_sent_list) < number_of_sentences:
            sent = random.choice(sentences)
            if sent not in gen_sent_list and sent != "":
                gen_sent_list.append(sent)
        return gen_sent_list


def countdown():
    for i in range(3, 0, -1):
        time.sleep(1)
        print(i)


def remove_spaces(sent):
    return ' '.join(list(sent)).split()


def compare_sentences(gen_sent, answer_sent):
    count = 0
    for x, y in zip(gen_sent, answer_sent):
        if x == y:
            count += 1
    return count


def validate_input(input_val):
    with open(file="sentences.txt", mode="w+") as sf:
        text = sf.readlines()
    max_len = len(text)

    if not input_val.isnumeric():
        print("Wrong type of input. Expected number.")
        return False
    elif int(input_val) < 0:
        print("Wrong argument. Expected value greater than 0.")
        return False
    elif int(input_val) > max_len:
        print(f"WARNING. Wrong number of sentences to select.\nMax value is {max_len}.")
        return False
    else:
        return True


def typing_program():
    create_history_file()

    info = input("Are you ready (yes/no):\n")
    if info not in ["yes", "no"]:
        print("Wrong option. Expected 'yes' or 'no'.")
        quit()
    elif info == "yes":
        num_of_sent = input("Enter the number of sentences: ")

        while not validate_input(input_val=num_of_sent):
            num_of_sent = input("Enter the number of sentences: ")

        n = int(num_of_sent)
        generated_sentences = get_random_sentence(number_of_sentences=n)

        for generated_sent in generated_sentences:
            countdown()
            char_count = len(remove_spaces(sent=generated_sent))

            print(generated_sent)

            start_time = datetime.now()
            answer = input("Type the sentence above:\n")
            end_time = datetime.now()
            count = compare_sentences(gen_sent=remove_spaces(generated_sent),
                                      answer_sent=remove_spaces(answer))
            time_taken = (end_time - start_time).total_seconds()

            accuracy = round((count / char_count) * 100, 2)
            wpm = round(((char_count / time_taken) * 60))

            print(f"wpm: {wpm} words / minute")
            print(f"accuracy: {accuracy} %")

            save_history(session=n, generated_sent=generated_sent,
                         answer=answer, time_taken=time_taken, accuracy=accuracy)
    else:
        print("Turning back to main menu.")


def option_validation(opt):
    opt_list = ["1", "2"]
    if not opt.isnumeric():
        print("WARNING. Wrong type of input. Expected number.")
        return False
    elif opt not in opt_list:
        print(f"WARNING. Wrong option. Expected option are: {', '.join(opt_list)}.")
        return False
    else:
        return True


def show_menu():
    menu_loop = 1
    while menu_loop == 1:
        print("[ ---- MENU ---- ]")
        print("[1] New session.")
        print("[2] Exit program.\n")

        option = input("Enter an option: ")
        print(type(option))
        while not option_validation(opt=option):
            option = input("Enter an option: ")

        if option == "1":
            typing_program()
        else:
            print("Closing program.")
            menu_loop = 0
