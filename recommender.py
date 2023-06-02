# This program will take a file with names of people, names of books,
# and ratings for those books by said people, then allow the user to
# do one of three things. They can request a book reccomendation
# for a specific user, get the average rating for all the books, or
# quit the program.

QUIT = 1
def main():
    # Initialize variables
    filename = 'ratings.txt'
    sentinel = 0
    ###Pre-Processing###
    file_list = read_file(filename)
    book_names_list = get_book_titles(file_list)
    ratings_dict = get_ratings_dict(book_names_list, file_list)
    ###Run Code###
    intro_message()
    while sentinel != QUIT:
        # prompt for user input
        next_task = input("next task? ")
        if next_task == 'quit':
            sentinel = QUIT
        elif next_task == 'averages':
            total_avg_rating_list = averages(book_names_list, ratings_dict)
            print_averages(total_avg_rating_list)

        elif next_task == 'recommend':
            try:
                current_usr = input('user? ')
                similarity_list = calc_similarity(ratings_dict, current_usr)
                avg_rating_list = recommend_books(similarity_list,
                                                  book_names_list, ratings_dict)
            except KeyError:
                avg_rating_list = averages(book_names_list, ratings_dict)
                
            print_averages(avg_rating_list)
        print()
            
    
    
###Pre-Processing###
    
# reads the file, and splits it into list with each element
# representing a line and return that list.
def read_file(filename):
    with open (filename) as file:
        file_list = file.readlines()
        for element in range (0, len(file_list)):
            file_list[element] = file_list[element].strip()
        return file_list

# take an argument of a list with all the lines from the file
# and create a set with all the book titles, then cast that set
# into a list and return that list.
def get_book_titles(file_list):
    book_names_set = set()
    for current_element in range(0,len(file_list), 3):
        current_book = file_list[current_element + 1].strip()
        book_names_set.add(current_book)
    book_names_list = list(book_names_set)
    return book_names_list

# Take the list of unique book names and list of whole file
# as an argument, then create a dictionary with each unique
# person's name as a key and the corresponding value as a list
# of 0s with length equal to that of the list of unique book names.
# Then reassign the rating values for each person to the rating they
# gave each book. Make sure in the list of values, the indices of the
# ratings correspond the correct book index in the list of unique book
# names. If the user has not rated a particular book, leave it as 0.
# Return the ratings dict.
def get_ratings_dict(book_names_list, file_list):
    ratings_dict = {}
    empty_ratings_list = []
    for book in range(0, len(book_names_list)):
        empty_ratings_list.append(0) 
    # Assign each person to the list of zeros then be replaced
    for current_name in range (0, len(file_list), 3):
        ratings_dict[file_list[current_name]] = empty_ratings_list

    # Reassign each person to be the correct list
    for current_name in range (0, len(file_list), 3):
        current_book = book_names_list.index(file_list[current_name + 1].strip())
        current_rating = int(file_list[current_name + 2])
        current_ratings_list = list(ratings_dict[file_list[current_name]])
        current_ratings_list[current_book] = current_rating
        ratings_dict[file_list[current_name]] = current_ratings_list
        
    return ratings_dict



###Get User Input###

# Output intro message
def intro_message():
    print("Welcome to the CS126 Book Recommender.\
    Type the word in the left column to d othe action on the right.")
    print("recommend : recommend books for a particular user")
    print("averages  : output the average ratings of all books in the system")
    print("quit      : exit the program")



###Averages###

# Accepts list of unique book names and dictionary with user names and
# corresponding books ratings as arguments. Create three empty dict.

# One that will store the book names as keys, and the values as the total
# of all non-zero ratings for that book. Another that will still store the
# book names as keys, and the count of non-zero ratings for said book. And
# a third that will also store the book names as keys, and the corresponding
# averages as values.
def averages(book_names_list, ratings_dict):
    ratings_total_dict = {}
    num_ratings_dict = {}
    avg_ratings_list = []
    
    # For each key in the input dict., systematically check the 0 index in the
    # list. If it is a 0, ignore; otherwise, add the value to the total ratings
    # dict. and add one to the value in the count dict.
    # Continue to do this for every index in the ratings list.
    for usr_name in ratings_dict.keys():
        for current_book_index in range (0, len(book_names_list)):
            current_list = ratings_dict[usr_name]
            current_rating = current_list[current_book_index]
            current_book = book_names_list[current_book_index]
            if current_rating != 0:
                if current_book in ratings_total_dict:
                    ratings_total_dict[current_book] += current_rating
                    num_ratings_dict[current_book] += 1

                else:
                    ratings_total_dict[current_book] = current_rating
                    num_ratings_dict[current_book] = 1                    

    # Divde the values in the total rating dict. by the corresponding values in
    # the count dict. and store this in the averages dict.
    for current_book in ratings_total_dict.keys():
        total_rating = ratings_total_dict[current_book]
        num_ratings = num_ratings_dict[current_book]
        if num_ratings != 0:
            avg_rating = total_rating/num_ratings
            avg_tuple = (avg_rating, current_book)
            avg_ratings_list.append(avg_tuple)
            avg_ratings_list.sort(reverse = True)
    # Return average ratings list
    return avg_ratings_list

# Print the names of the books and their corresponding average ratings, with
# each book beginning on a new line.
def print_averages(avg_ratings_list):
    for book in range(0, len(avg_ratings_list)):
        print(avg_ratings_list[book][1], avg_ratings_list[book][0])



###Recommendations###
        
### This will require two functions. One to calculate similarity between
### given user and other users. And one to take the top three most similar
### users and gather a book recommendation from them

###Function 1###
# Accept the dict. of users and corresponding ratings as an argument.
def calc_similarity(ratings_dict, current_usr):

    # initialize variables
    usr_ratings_list = ratings_dict[current_usr]
    
    # Create empty list which will store tuples with other users and their
    # similarity rating.
    similarity_list = []

    # Systematically compare the list of ratings for our particular user with
    # the list of ratings for each other user. Do this by multiplying
    # corresponding indices and summing all of these products for each other user
    # Then store these values as tuples in the form (similarity rating, user name)
    # in the simlarity ratings list we initilized previously.
    for usr in ratings_dict.keys():
        ratings_list = ratings_dict[usr]
        if usr != current_usr:
            similarity_rating = 0
            for current_rating in range(0, len(ratings_list)):
                similarity_rating += usr_ratings_list[current_rating]\
                                        * ratings_list[current_rating]
            similarity_list.append((similarity_rating, usr))

    # Sort the list in order from highest to lowest similarity and return this
    # list
    similarity_list.sort(reverse = True)
    return similarity_list


###Function 2###
# Accept the list from the previous function, the list of unique book names,
# and the dict. of users and ratings as arugments.
def recommend_books(similarity_list, book_names_list, ratings_dict):
    similar_usrs_list = []
    similar_ratings_dict = {}
    negative_count = 0
    
    # Get the first three tuples from the similarity list and store only the
    # names in a new list of similar users
    for usr in range(0, 3):
        similar_usrs_list.append(similarity_list[usr][1])

    # Create a new dictionary using the dict. of users and ratings that only
    # contains they keys of the three most similar users and their corresponding
    # ratings.
    for usr in similar_usrs_list:
        similar_ratings_dict[usr] = ratings_dict[usr]

    # Call to the averages function and use the new dict. as the argument,
    # as well as the list of unique book names.
    similar_avg_ratings = averages(book_names_list, similar_ratings_dict)

    #remove any book that is negative
    for current_index in range(0,len(similar_avg_ratings)):
        current_sim_rating = similar_avg_ratings[current_index][0]
        if current_sim_rating < 0:
            negative_count += 1
    positive_similar_avg_ratings = similar_avg_ratings[:len(similar_avg_ratings) - negative_count]
    # Return this list
    return positive_similar_avg_ratings

main()












