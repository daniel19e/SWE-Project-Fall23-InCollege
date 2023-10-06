
from util import clear_terminal, inspect_input
from auth import create_account, get_current_username
from ascii_art import aa_error404
from database import get_existing_db_object

db = get_existing_db_object()
# this is a general function that will display any link page
def display_link_page(page_name, link_name_list, link_function_list):
    while True:
        clear_terminal()
        print(f"{page_name}\n")
        for i, link in enumerate(link_name_list):
            print(f"{i+1}. {link}")
        print("\n0. Go Back")
        selection = input("\nWhich link would you like to access: ")
        if selection == "0":
            clear_terminal()
            break
        try:
            # call corresponding function
            link_function_list[int(selection) - 1]()
        except:
            clear_terminal()
            print("Invalid link\n")


def about_page():
    clear_terminal()
    print("In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide")
    input("Enter any input to go back: ")


def help_center_page():
    clear_terminal()
    print("We're here to help")
    input("Enter any input to go back: ")


def press_page():
    clear_terminal()
    print("In College Pressroom: Stay on top of the latest news, updates, and reports")
    input("Enter any input to go back: ")


def blog_page():
    clear_terminal()
    print(aa_error404)
    print("Oops! Under construction 🛠️\n")
    input("Enter any input to go back: ")


def careers_page():
    clear_terminal()
    print(aa_error404)
    print("Oops! Under construction 🛠️\n")
    input("Enter any input to go back: ")


def developers_page():
    clear_terminal()
    print(aa_error404)
    print("Oops! Under construction 🛠️\n")
    input("Enter any input to go back: ")


def sign_up_page():
    clear_terminal()
    print("Sign Up (Enter X to cancel)")

    firstname = input("Enter your first name: ")
    if inspect_input(firstname):
        clear_terminal()
        return False

    lastname = input("Enter your last name: ")
    if inspect_input(lastname):
        clear_terminal()
        return False

    username = input("Enter new username: ")
    if inspect_input(username):
        clear_terminal()
        return False
    password = input("Enter new password: ")
    if inspect_input(password):
        clear_terminal()
        return False
    
    major = input("Enter your major: ")
    if inspect_input(major):
        clear_terminal()
        return False
    
    university = input("Enter your university: ")
    if inspect_input(university):
        clear_terminal()
        return False

    clear_terminal()

    create_account(db, username, password, firstname, lastname, major, university)
    return True


def general_link():
    clear_terminal()
    user = db.get_user_info(get_current_username())
    if (user):
        general_link_names = ["Help Center", "About",
                            "Press", "Blog", "Careers", "Developers"]
        general_links_functs = [help_center_page, about_page, press_page, blog_page, careers_page, developers_page]
    else:
        general_link_names = ["Sign Up", "Help Center", "About",
                            "Press", "Blog", "Careers", "Developers"]
        general_links_functs = [sign_up_page, help_center_page,
                                about_page, press_page, blog_page, careers_page, developers_page]
    display_link_page("General links", general_link_names,
                      general_links_functs)


def browse_incollege_link():
    clear_terminal()
    print(aa_error404)
    print("Oops! Under construction 🛠️\n")
    input("Enter any input to go back: ")


def business_solutions_link():
    clear_terminal()
    print(aa_error404)
    print("Oops! Under construction 🛠️\n")
    input("Enter any input to go back: ")


def directories_link():
    clear_terminal()
    print(aa_error404)
    print("Oops! Under construction 🛠️\n")
    input("Enter any input to go back: ")

def show_page_with_message(title, message):
    clear_terminal()
    print(title)
    print(message)
    input("Enter any input to go back: ")

def show_guest_controls():
    clear_terminal()
    user = db.get_user_info(get_current_username())
    if user:
        print("Guest Controls \n")
        print("-------------------------------------")
        print("Receive Emails: ", ("No" if user[6] == 0 else "Yes"))
        print("Receive SMS: ", ("No" if user[7] == 0 else "Yes"))
        print("Targeted Advertisments: ", ("No" if user[8] == 0 else "Yes"))
        print("-------------------------------------")

        print("\nToggle the settings with the following options: \n")
        print("1. Receive Emails")
        print("2. Receive SMS")
        print("3. Targeted Advertisments")

        print("\n0. Go back\n")

        choice = input("Enter option: ")

        if choice == '0':
            return
        if choice == '1':
            db.get_cursor().execute("UPDATE college_students SET receive_emails = ? WHERE username = ?", (not user[6], get_current_username()) )
            db.get_connection().commit()
        if choice == '2':
            db.get_cursor().execute("UPDATE college_students SET receive_sms = ? WHERE username = ?", (not user[7], get_current_username()) )
            db.get_connection().commit()
        if choice == '3':
            db.get_cursor().execute("UPDATE college_students SET targeted_ads = ? WHERE username = ?", (not user[8], get_current_username()) )
            db.get_connection().commit()
        show_guest_controls()
    else:
        print("Guest Controls\n")
        print("This is only available to logged in users.\n");
        input("Enter any input to go back: ")

def show_languages():
    clear_terminal()
    user = db.get_user_info(get_current_username());
    if user:
        print("Languages\n")
        print("Current language: " + user[5]);
        print("\nSelect language:")
        print("1. English")
        print("2. Spanish")
        print("\n0. Go back\n")
        choice = input("Enter which language you would like to select: ")
        if choice == '0':
            return
        if choice == '1':
            db.get_cursor().execute("UPDATE college_students SET language = 'english' WHERE username = ?", (get_current_username(),) )
            db.get_connection().commit()
        if choice == '2':
            db.get_cursor().execute("UPDATE college_students SET language = 'spanish' WHERE username = ?", (get_current_username(),) )
            db.get_connection().commit()
        show_languages()
    else:
        print("Languages\n")
        print("We support 2 different languages: English and Spanish.");
        print("Once you have created an account, you will be able to choose which one you want to use.\n");
        input("Enter any input to go back: ")

def show_copyright_notice():
    clear_terminal()
    print("Copyright Notice")
    print("© 2023 InCollege, Inc. All rights reserved. The content, graphics, and other elements of this website are protected under copyright law and may not be reproduced, distributed, transmitted, displayed, published, or broadcast without the prior written permission of InCollege, Inc. or in the case of third party materials, the owner of that content. Unauthorized use or infringement may result in legal action.")
    input("Enter any input to go back: ")

def show_about():
    clear_terminal()
    print("About")
    print("In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide.")
    input("Enter any input to go back: ")

def show_accessibility():
    clear_terminal()
    print("Accessibility")
    print("InCollege, Inc. is committed to ensuring that our website is accessible to everyone, regardless of ability or technology. We are actively working to enhance the accessibility and usability of our content, and in doing so, adhere to many of the available standards and guidelines. Should you experience any difficulty in accessing any part of this website, please don't hesitate to contact us.")
    input("Enter any input to go back: ")

def show_user_agreement():
    clear_terminal()
    print("User Agreement")
    print("By using the InCollege website and its associated services, you agree to comply with all applicable laws and our terms of service. You are responsible for maintaining the confidentiality of your account and for any activities that occur under your account. InCollege, Inc. reserves the right to modify or terminate services, content, or user accounts at its discretion.")
    input("Enter any input to go back: ")

def show_privacy_policy():
    clear_terminal()
    print("Privacy Policy")
    print("InCollege, Inc. values and respects your privacy. We collect and use your personal information solely for the purpose of enhancing your experience and to provide specific services you request. Your data will never be shared or sold to third parties without your explicit consent. Cookies and other tracking technologies may be used to improve the user experience. By using our website, you consent to our privacy practices.")
    input("Enter any input to go back: ")

def show_cookie_policy():
    clear_terminal()
    print("Cookie Policy")
    print("InCollege, Inc. utilizes cookies to enhance your browsing experience and deliver personalized content. By visiting our website, you agree to the use of cookies as described in this policy. You can adjust your browser settings to refuse cookies or alert you when they are being sent, although this may affect the functionality and performance of our site.")
    input("Enter any input to go back: ")

def show_copyright_policy():
    clear_terminal()
    print("Copyright Policy")
    print("All content, designs, graphics, and other materials published by InCollege, Inc. on our website are protected by copyright law. Unauthorized use, reproduction, distribution, or modification of this copyrighted material without the express written permission of InCollege, Inc. is strictly prohibited. If you believe any content on our site infringes upon your copyright, please contact us immediately.")
    input("Enter any input to go back: ")

def show_brand_policy():
    clear_terminal()
    print("Brand Policy")
    print("Copyright © 2023 InCollege, Inc.; all content is protected by law, and unauthorized use or reproduction without our express permission is prohibited.")
    input("Enter any input to go back: ")


def show_useful_links():
    clear_terminal()
    useful_link_names = ["General", "Browse InCollege",
                         "Business Solutions", "Directories"]
    useful_links_functs = [general_link, browse_incollege_link,
                           business_solutions_link, directories_link]
    display_link_page("Useful links", useful_link_names, useful_links_functs)


def show_incollege_important_links():
    clear_terminal()
    important_link_names = ["A Copyright Notice", "About", "Accessibility", "User Agreement", "Privacy Policy",
                            "Cookie Policy", "Copyright Policy", "Brand Policy", "Guest Controls", "Languages"]
    important_links_functs = [
        show_copyright_notice,
        show_about,
        show_accessibility,
        show_user_agreement,
        show_privacy_policy,
        show_cookie_policy,
        show_copyright_policy,
        show_brand_policy,
        show_guest_controls,
        show_languages
    ]  # need to implement

    display_link_page("Important links", important_link_names,
                      important_links_functs)