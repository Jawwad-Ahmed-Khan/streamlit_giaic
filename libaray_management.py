import json
import os
def Add_Book():
    entity_Book = {
        "Title":"",
        "Author": "",
        "Publication":"",
        "Genre":"", 
        "Read_Status": False
    }
    
    entity_Book["Title"] = input("Enter The Book Title: ")
    entity_Book["Author"] = input("Enter The Author Name: ")
    entity_Book["Genre"] = input("Enter The Genre of Book: ")
    entity_Book["Publication"] = input("Enter The Publication year of Book:")
    json_data = json.dumps(entity_Book,indent=5)
    
    with open("library_books.txt","a") as file:
        file.write(json_data + "\n" )

    return "Book Successfully Added In Library"

def search_book():

    book_name = input("Enter The Book Title: ")
    
    try:
        with open("library_books.txt", "r") as file:
            for line in file:
                book = json.loads(line.strip())  # Convert JSON string to dictionary
                
                if book["Title"] == book_name:  # ✅ Correct dictionary access
                    return book  # Return the book if found

    except FileNotFoundError:
        print("Error: The file 'library_books.txt' does not exist.")
    except json.JSONDecodeError:
        print("Error: The file contains invalid JSON format.")

    return "The book is Not Found"  # If no book matches, return this   

def remove_book():
    book_name = input("Enter The Book Title: ")
    book_file = "library_books.txt"
    
    books = []  # List to store remaining books
    book_found = False  # Flag to check if the book exists

    try:
        # Check if the file exists
        if not os.path.exists(book_file):
            raise FileNotFoundError("Error: The file does not exist.")

        with open(book_file, "r") as file:
            for line in file:
                try:
                    book = json.loads(line.strip())  # Convert JSON to dict
                    if book["Title"] == book_name:
                        book_found = True  # Book found, skip adding it
                        continue
                    books.append(book)  # Add other books to the list
                except json.JSONDecodeError:
                    print("Warning: Skipping a line due to invalid JSON format.")

        # If book was found, update the file
        if book_found:
            with open(book_file, "w") as file:
                for book in books:
                    file.write(json.dumps(book) + "\n")  # Write back valid books
            
            print(f"Book '{book_name}' has been removed successfully.")
        else:
            print(f"Book '{book_name}' not found.")

    except FileNotFoundError as e:
        print(e)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def Display_all_books():
   
    try:
        
        if not os.path.exists("library_books.txt"):
            raise FileNotFoundError("The file 'library_books.txt' does not exist.")

        with open("library_books.txt", "r") as file:
            content = file.read().strip() 
        
            if not content:  
                raise ValueError("The file is empty.")

            books = json.loads(content)  

        return books  

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return []  

    except json.JSONDecodeError:
        print("Error: Invalid JSON format in file.")
        return []  

    except ValueError as e:
        print(f"Error: {e}")
        return [] 

def Display_statistics():
    pass


def Operation_perform(select_operation):


    if select_operation == 1:
        return Add_Book()
    elif select_operation == 2:
        return search_book()
    elif select_operation == 3:
        return remove_book()
    elif select_operation == 4:
        return Display_all_books()
    elif select_operation == 5:
        return Display_statistics()
    elif select_operation==6:
        exit()
    else :
        return " ------- | Select The Right Option | ----------"








def Menu():
    print("1:Add a Book")
    print("2:Search for  a Book")
    print("3:Remove a Book")
    print("4:Display All Books")
    print("5: Display Statistics")
    print("6:Exit")


while True:
    Menu()
    operation = int(input("Enter Your Choice: "))
    os.system("cls")
    print(Operation_perform(operation))