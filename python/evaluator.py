import numpy as np
from matplotlib import pyplot as plt 
from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections

# Prompts user until he answers the questions with yes or no 
def get_answer():
    answer = str(input()).lower()
    while (answer != "yes" and answer != "no"):
        print("Please enter \'yes\' or \'no\'", end="\n\n")
        answer = str(input()).lower()

    if (answer == "yes"):
        print("We would recommend seeing a medical professional about this issue.")
    return answer == "yes"

def categorize(segment):

    responses = ["The system has identified a cold sore on your lip. This may indicate a Herpes Simplex viral infection- please answer the following questions for us to advise you on the best course of action.", "The system has identified a chancre sore on your tongue. This may indicate syphilis - please answer the following questions for us to advise you on the best course of action.", "The system has identified a thick white depot on your tongue. This may indicate a range of different things. Please answer the following questions for us to advise you on the best course of action.", "The system has identified dark patches on your gums. This indicates there is a high probability of oral cancer. Go see your GP."]
    questions = [["1/5 - Have you had this for over 10 days?", "2/5 - Is it very painful?", "3/5 - Unexplained weight loss?", "4/5 - Are you pregnant? ", "5/5 - Have you got a weakened immune system due to chemotherapy, diabetes, or other?"], ["1/3 - Do you have similar sores in your genital areas (penis, vagina, around the anus)?", "2/3 - Do you have a blotchy red rash on the palms of your hands or soles of your feet?", "3/3 - tiredness, headache, joint pain?"], ["1/5 - Cleans away? Disapears?", "2/5 - Is it painful or itchy?", "3/5 - Has this lasted more than 10 days?", "4/5 - HasWorsening?", "5/5 - Unexplained weight loss"], [""]]
    final = ["No need to worry for now. If the sore hasn’t started to heal 10 days after you first noticed it, go see your GP.", "This lesion does not seem worrying for now. If this chancre doesn’t disappear within 2 weeks, or if any of the previously mentioned symptoms appear, go see your GP for a check-up.", "Nothing to worry about.", ""]

    for i,f in enumerate(list(segment)):
        if f == '0':
            continue
        print("\n\n" + responses[i], end="\n\n")
        for q in questions[i]:
            print(q)
            if (i != 3 and get_answer()): return
        print("\n" + final[i])


def main():
    # segment = [input() for _ in range(5)]
    segment = "1001"
    categorize(segment)

if __name__ == '__main__':
 main()