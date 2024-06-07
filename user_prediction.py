# NAME: Nick Marker
# ID: 4392033540
# DATE: 05/04/2023
# DESCRIPTION: This program analyzes various data sets (in this case 4) that were each generated using AI. These data
# sets each contain a set of keywords, each aligning with a specific percentage representing the likelihood that the
# keyword relates to the specific demographic at the head of the column with the percent. This program is a very basic,
# hard coded form of using programming to make predictions. The keywords used to make the predictions stem from societal
# stereotypes that are generalized, and may not be true to the specific user using the program. The program analyzes
# these percentages to provide the most likely predictions for the user, based on their mock Google searches.

from typing import List, Tuple
from itertools import islice

# allows all user data to be saved to a specific instance and printed as one, rather than concatenating a long string
# to pass through functions and return
class User:
    def __init__(self, name: str, age: str, gender: str, marital_status: str, salary: str):
        """Ensures that a user instance is only created when parameters such as the name, age, gender, marital status,
        and salary are provided. These can be set to 'unknown' for temporary instantiation, prior to predictions.
        """
        self.name = name
        self.age = age
        self.gender = gender
        self.marital_status = marital_status
        self.salary = salary

    def __str__(self) -> str:
        """Returns all basic predictions when a user is printed. Information includes the user's age, gender, marital
        status, and salary.
        """
        user_printed = "\nPredictions for " + self.name + " are as follows: \nAge: " + self.age + "\nGender: " + \
                       self.gender + "\nMarital Status: " + self.marital_status + "\nSalary: " + str(self.salary)

        return user_printed


# function found in library to aid with finding the second instance of a value, rather than just the first
def nth_index(iterable: list[str], value: str, n: int) -> int:
    """Function found in a programming library to help find the nth index of a character in a list, as opposed to using
    only .index(), which provides the first instance only. Parameters include the list you are searching through, the
    value you are looking for, and the nth occurrence that you would like to find (i.e 2nd, 3rd, etc.).
    """
    matches = (idx for idx, val in enumerate(iterable) if val == value)

    return next(islice(matches, n-1, n), None)


# asks user for 3 Google searches and returns a list of length 3 --> the three searches
def retrieve_searches() -> List[str]:
    """Prompts user for the 3 needed Google searches to analyze for keywords. Combines all searches into one list and
    returns such list.
    """
    user_searches = []
    input("\nI will need three mock Google searches corresponding to the user personas previously described. Press "
          "enter to continue.")
    # strips all searches to remove unnecessary spacing
    search1 = input("\nPlease enter your first mock Google search: ").strip()
    while search1 == '':
        search1 = input("\nPlease enter your first mock Google search: ").strip()
    search2 = input("Please enter your second mock Google search: ").strip()
    while search2 == '':
        search2 = input("\nPlease enter your second mock Google search: ").strip()
    search3 = input("Please enter your third mock Google search: ").strip()
    while search3 == '':
        search3 = input("\nPlease enter your third mock Google search: ").strip()

    user_searches.append(search1)
    user_searches.append(search2)
    user_searches.append(search3)

    return user_searches


# analyzes user search to make a list of all keywords used
def get_keywords_from_user_search(search_list: List[str], file_with_keywords) -> List[str]:
    """Analyzes the list of searches from the user to extract any keywords used. These keywords are found in the first
    column of the corresponding data file. Keywords can be found even if in the plural form (i.e. Career vs. Careers).
    Returns a list of all the keywords used.
    """
    keywords_used = []
    f = open(file_with_keywords, 'r')
    line = f.readline()
    temp_line = line.split(',')

    # iterates through entire data file (all keywords in data file)
    while line != '':
        for search in search_list:
            temp_search = search.split(' ')
            for word in temp_search:
                if temp_line[0].lower() == word.lower() or temp_line[0].lower() + 's' == word.lower() or \
                        temp_line[0].lower() + 'ing' == word.lower():
                    # ensures keyword is not added twice to the list of keywords used
                    if temp_line[0] not in keywords_used:
                        keywords_used.append(temp_line[0])
        line = f.readline()
        temp_line = line.split(',')

    return keywords_used


# return dictionary in format keyword: [(percentage1 index, percentage2 index),...]
def create_percentage_dictionary(search_list: List[str], file_with_keywords: str) -> dict[str, List[Tuple[int, int]]]:
    """Creates a dictionary with each key being the keywords used by the user in the 3 searches, and the values being
    the two highest percentages corresponding to that keyword, and the index of these percentages (column).
    """
    f = open(file_with_keywords, 'r')
    line = f.readline()
    temp_line = line.split(',')
    keyword_percentages = {}
    keyword_percentage_index = {}

    keywords_used = get_keywords_from_user_search(search_list, file_with_keywords)

    while line != '':
        for i in range(len(keywords_used)):
            if temp_line[0] == keywords_used[i]:
                # uses the top two highest percentages and their indexes only
                keyword_percentages[keywords_used[i]] = find_max_percentages_index(keywords_used[i], file_with_keywords)
                keyword_percentage_index[keywords_used[i]] = \
                    find_max_percentages_index(keywords_used[i], file_with_keywords)

        line = f.readline()
        temp_line = line.split(',')

    return keyword_percentage_index


# finds the top 2 percentages of each keyword along with the index of these percentages
def find_max_percentages_index(keyword: str, file_with_keywords: str) -> List[Tuple]:
    """Using a specific keyword and the data file corresponding to such keyword, returns the two highest percents
    corresponding to that keyword, in addition to the index of the two highest percents (column).
    """
    f = open(file_with_keywords, 'r')
    line = f.readline()
    temp_line = line.split(',')
    # initializes the percent and percent index variables
    max_percent = 0
    max_percent_2 = 0
    max_percent_index = 0
    max_percent_2_index = 0

    while line != '':
        if temp_line[0] == keyword:
            for i in range(1, len(temp_line)):
                if int(temp_line[i]) >= max_percent and int(temp_line[i]) >= max_percent_2:
                    max_percent_2 = max_percent
                    max_percent = int(temp_line[i])
                    max_percent_index = temp_line.index(temp_line[i])
                    # attempts to assign an index corresponding to the second-highest percent, but there may not be a
                    # second-highest percent yet to index
                    try:
                        max_percent_2_index = temp_line.index(str(max_percent_2))
                        if max_percent_2_index == max_percent_index:
                            max_percent_2_index = nth_index(temp_line, str(max_percent_2), 2)
                    except ValueError:
                        pass
                        # print("---no index for max_percent_2 yet---ignore")  # can uncomment to show user attempts
                elif int(temp_line[i]) >= max_percent_2:
                    max_percent_2 = int(temp_line[i])
                    max_percent_2_index = temp_line.index(temp_line[i])

        line = f.readline()
        temp_line = line.split(',')

    return [(max_percent, max_percent_index), (max_percent_2, max_percent_2_index)]


# finds the top two highest percents from all keywords along with their index
def compare_percentages(keyword_percentage_index: dict[str: List[Tuple[int, int]]]) -> List[Tuple[int, int]]:
    """Using the dictionary of keywords, percentages, and indexes, returns the two highest percentages across all
    keywords, in addition to the indexes (columns) corresponding to these highest percentages. If percentages too broad,
    will only return the highest.
    """
    highest_percent = 0
    highest_percent_index = 0
    highest_percent_2 = 0
    highest_percent_2_index = 0

    for keyword in keyword_percentage_index:
        # new percent becomes the highest if greater than the highest and second highest
        if keyword_percentage_index[keyword][0][0] >= highest_percent and keyword_percentage_index[keyword][0][0] >= \
                highest_percent_2:
            highest_percent_2 = highest_percent
            highest_percent = keyword_percentage_index[keyword][0][0]
            highest_percent_2_index = highest_percent_index
            highest_percent_index = keyword_percentage_index[keyword][0][1]
        # new percent becomes second highest if only greater than the second highest
        elif keyword_percentage_index[keyword][0][0] >= highest_percent_2:
            highest_percent_2 = keyword_percentage_index[keyword][0][0]
            highest_percent_2_index = keyword_percentage_index[keyword][0][1]

    highest_percents = [(highest_percent, highest_percent_index), (highest_percent_2, highest_percent_2_index)]
    # if percents are greater than 10% apart, will only use the higher percent for prediction
    highest_percents = narrow_percent(highest_percents)

    return highest_percents


# if two highest percents are greater than 10% apart, only the highest one will be used for analysis
def narrow_percent(highest_percents: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Checks to see if the two highest percents identified are greater than 10% apart. If so, will only return the
    higher percent and its index, if not, will return both percents and their indexes.
    """
    percent1 = highest_percents[0][0]
    percent2 = highest_percents[1][0]
    # only returns the highest percent and its index of percents are greater than 10% apart
    if abs(percent1 - percent2) >= 10:
        greatest_percent = max(percent1, percent2)
        if greatest_percent == percent1:
            return [(percent1, highest_percents[0][1])]
        elif greatest_percent == percent2:
            return [(percent2, highest_percents[1][1])]

    return highest_percents


# using the index of the highest percents, returns the corresponding predicted age range
def find_age_range(highest_percents: List[Tuple[int, int]], file_with_keywords: str) -> str:
    """Uses the two highest percents and their indexes to find the two most likely age ranges based on the initial
    keywords used, only one age range if only one highest percent is provided. If two age ranges are identified, will
    return the combination of such ranges (i.e. 0-17 and 18-24 would return 0-24).
    """
    suggested_age_range = []
    f = open(file_with_keywords, 'r')
    line = f.readline()
    age_ranges = line.split(',')

    # if no keyword for the age data is given, return 'unknown' for age prediction
    if highest_percents == [(0, 0), (0, 0)]:
        predicted_age = 'unknown'
        return predicted_age

    for item in highest_percents:
        col = item[1]
        # in data table all ages are in the age-age format, so splitting them using "-"
        temp_age_range = age_ranges[col].split('-')
        suggested_age_range.append(temp_age_range[0])
        suggested_age_range.append(temp_age_range[1])

    suggested_age_range.sort()
    # finds min and max out of all the ages in the age ranges, and creates a new range with a new min and max
    max_range = max(suggested_age_range)
    min_range = min(suggested_age_range)

    # returns adjusted age range prediction
    predicted_age = min_range + "-" + max_range

    return predicted_age


# using the index of the highest percents, returns the corresponding predicted salary
def find_characteristic(highest_percents: List[Tuple[int, int]], file_with_keywords: str) -> str:
    """Uses the two highest percents and their indexes to find the demographic characteristic that is most likely based
    on the percents. Uses the index of the higher percent to find the predicted characteristic.
    """
    f = open(file_with_keywords, 'r')
    line = f.readline()
    characteristics = line.split(',')

    higher_percent = highest_percents[0][0]
    higher_percent_index = highest_percents[0][1]
    for item in highest_percents:
        if item[0] >= higher_percent:
            higher_percent = item[0]
            higher_percent_index = item[1]

    # assigns character to 'unknown' if user did not enter a keyword that triggers any specific demographic for that
    # characteristic
    if highest_percents == [(0, 0), (0, 0)]:
        suggested_char = 'unknown'
    else:
        suggested_char = characteristics[higher_percent_index]

    # assigned to a new variable that is returned to provide the option for future manipulation to the characteristic
    # similar to the manipulation to the age range characteristic
    predicted_char = suggested_char

    return predicted_char


def explain_program() -> None:
    """Explains the outline of the program to the user, and a rough idea on how to 'play'. Also provides an option to
    see an example, which will provide user's with a rough idea on how to use the program, and what keywords to use.
    """
    input("Hi, welcome to my user prediction program! This program works by taking in 3 mock 'Google Searches' from the"
          " user (you), and provides a predicted user \ndemographic including age, gender, marital status, and salary. "
          "These predictions are based on the keywords detected in these Google searches. \nPress enter to continue.")
    see_example = input("\nIf you would like to see an example of how this program works, press 1. This example will "
                        "include a user persona, and the corresponding \nkeywords that the specific persona type would "
                        "use in their Google searches. This is highly recommended for first-time users. \nPress 1 to "
                        "see an example or enter to continue.")
    # provides an example search and prediction response to the user
    if see_example == '1':
        user_personas()
    input("\nFollowing the example provided, or a similar ideology, will allow for best results from the program. If "
          "the searches provided provide a too wide range of keywords, \nthe program will not be able to provide a "
          "specific prediction.\n")


def user_personas() -> None:
    """If the option to see an example is requested, will provide the user with an example user mock search and the
    sample predicted outcomes.
    """
    # hard coded instance of a User object
    # uses __str__ class User function to easily print the predictions of the user
    example_user1 = User('Colin', '0-17', 'Male', 'Single', 'Upper-Class')
    input("\nThe following example persona, 'Colin', provided the following Google searches to obtain a prediction:\n"
          "1. Tutorial for investing in cars\n"
          "2. Most popular fashion when gaming\n"
          "3. Travel plans for popular ski mountains\n"
          "Keywords used: invest, car, fashion, gaming, travel, ski\n" + str(example_user1) +
          "\nPress enter to continue.")


def save_prediction(current_user: User) -> None:
    """Save the user's set of predictions to an external file of their choice. File will be added to directory after
    the program exits its runtime.
    """
    # ensures user enters a filename to save to
    new_file = ''
    while new_file == '':
        new_file = input('Enter the filename of the .txt file you would like to save the prediction to: ').strip()

    # writes predictions to new file that will be saved
    f = open(new_file, 'w')
    f.write(str(current_user))

    f.close()

    print("Predictions saved to " + new_file)


def main():
    # list of all data files used -> one per predicted characteristic
    # this can be added to in the future to predict more characteristics
    data = ['data/age_keyword_data.csv', 'data/gender_keyword_data.csv', 'data/salary_keyword_data.csv', 'data/marital_keyword_data.csv']
    # takes in name of user to feel more personable and specific when providing predictions
    user_name = input("Welcome! Please enter your name: ")
    while user_name == '':
        user_name = input("Welcome! Please enter your name: ")
    # instantiates instance of the User class with temporary "unknown" parameter values
    current_user = User(user_name, "unknown", "unknown", "unknown", "unknown")
    explain_program()

    # will continue to play game as long as user continues to respond with "y"
    play_again = 'y'
    while play_again == 'y':
        search_list = retrieve_searches()

        # iterates through each data file, predicting each characteristic individually
        for file in data:
            keyword_percentage_index = create_percentage_dictionary(search_list, file)
            highest_percents = compare_percentages(keyword_percentage_index)
            if file == 'data/age_keyword_data.csv':
                user_age_range = find_age_range(highest_percents, 'data/age_keyword_data.csv')
                # assigns prediction to parameter of the current_user User object
                current_user.age = user_age_range.strip()
            elif file == 'data/gender_keyword_data.csv':
                user_gender = find_characteristic(highest_percents, 'data/gender_keyword_data.csv')
                # assigns prediction to parameter of the current_user User object
                current_user.gender = user_gender.strip()
            elif file == 'data/marital_keyword_data.csv':
                user_marital_status = find_characteristic(highest_percents, 'data/marital_keyword_data.csv')
                # assigns prediction to parameter of the current_user User object
                current_user.marital_status = user_marital_status.strip()
            elif file == 'data/salary_keyword_data.csv':
                user_salary = find_characteristic(highest_percents, 'data/salary_keyword_data.csv')
                # assigns prediction to parameter of the current_user User object
                current_user.salary = user_salary.strip()

        # prints the predictions without having to concatenate a result, because all data saved in current_user object
        print(current_user)

        # will save prediction to an external .txt file if the user wishes
        save = input('\nWould you like to save your prediction? '
                     '("s" for yes, all other inputs assume no): ').strip().lower()
        if save == 's':
            save_prediction(current_user)

        # program will continue asking for searches and providing predictions as long as the user replies "y"
        play_again = input('\nWould you like to receive another prediction? ("y" for yes): ').strip().lower()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()
