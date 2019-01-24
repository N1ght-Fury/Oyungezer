import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

import Post_Database
import User_Database
import Inform_User

Post = Post_Database.Database_Post()
Mail = User_Database.Database_User()


print("""
Enter '1' to organize user database.
Enter '2' to start the program.
Enter 'q' to exit program.
""")

while True:

    number = input("Command: ")

    if (number == "1"):

        print("""
        Enter '1' to see all users.
        Enter '2' to add a new user.
        Enter '3' to delete a user.
        Enter '4' to update a user.
        Enter '5' to see total number of users.
        Enter '6' to go back to main menu.
        Enter 'q' to exit the program.
        """)

        while True:

            command = input("\nCommand for mail: ")

            if (command == "1"):
                Mail.show_mails()

            elif (command == "2"):
                print("Enter a new mail address:")
                new_mail = input().lower()

                if (Mail.check_if_mail_exists(new_mail)):
                    print("\n" + new_mail,"already exists on database. Please try again.\n")
                    continue

                print("Would you want to receive mails? (Y/N):")
                user_stat = input().upper()

                if (user_stat == "Y"):
                    user_stat = True
                    text = new_mail + " successfully added to database."

                elif (user_stat == "N"):
                    user_stat = False
                    text = new_mail + " successfully added to database. Be aware that you wont receive any mails."

                else:
                    print("\nInvalid command. Try again.\n")
                    continue

                new_user = User_Database.User(new_mail,user_stat)
                Mail.add_mail(new_user)

                print(text)


            elif (command == "3"):

                if (Mail.total_user() == 0):
                    print("\nNo user found on database.\n")
                    continue

                print("Enter the mail address you want to delete:")
                del_mail = input("Mail: ")

                if (Mail.check_if_mail_exists(del_mail) == 0):
                    print("There is not such mail address as " + del_mail + ". Please try again")
                    continue

                print("Are you sure you want to delete " + del_mail + "? (Y/N):")
                yes_no = input().upper()

                if (yes_no == "Y"):
                    Mail.delete_mail(del_mail)
                    print(del_mail," successfully deleted from database.")

                elif (yes_no == "N"):
                    print("Process canceled.")
                    continue
                else:
                    print("\nInvalid command. Please try again.")


            elif (command == "4"):

                if (Mail.total_user() == 0):
                    print("\nNo user found on database.\n")
                    continue

                print("Enter the mail address you want to update: ")
                update_mail = input()

                if (Mail.check_if_mail_exists(update_mail) == 0):
                    print("There is not such mail address as " + update_mail + ". Please try again")
                    continue

                print("What would you want to change? "
                      "To go back, enter 'q' , to change mail, "
                      "enter M, to change status, enter S:")

                change_what = input().upper()

                # Updating User Mail
                if (change_what == "M"):
                    new_mail = input("Enter a new mail address: ")
                    Mail.update_mail(update_mail,new_mail)
                    print(update_mail, "changed to", new_mail + ".")

                # Updating Status (if 0, wont receive mails, else will)
                elif (change_what == "S"):
                    print("Would you want to get mails or not? (Y/N)")
                    yes_no = input().upper()
                    if (yes_no == "Y"):
                        Mail.update_stat(update_mail, True)
                        print(update_mail, "will now receive mails.")
                    elif (yes_no == "N"):
                        Mail.update_stat(update_mail, False)
                        print(update_mail, "will not receive mails anymore.")
                    else:
                        print("Wrong command. Please try again.")
                        continue

                elif (change_what == "Q"):
                    print("You are back to menu.")

                else:
                    print("\nInvalid comamnd. Try again.\n")


            elif (command == "5"):

                total = Mail.total_user()

                if (total != 0):
                    print("Total number of users: ",total)
                else:
                    print("No user found on database.")

            elif (command == "6"):
                # Going Back to Main Menu
                print("\nYou are on main menu right now.\n")
                break

            elif (command == "q"):
                exit()

            else:
                print("Invalid command. Try again.")


    elif (number == "2"):

        run_time = 0
        total_posts = 0

        while True:

            new_posts = 0

            #Checking if there are any users on database
            if (Mail.total_user() == 0):

                print("No user found on database. You have to add at least one user to continue.")
                user_mail = input("Mail: ").lower()
                print("Would you want to receive mails?")
                print("(If you are running this program for the first time, \nwe recommend "
                      "turning notifications off if you don't\nwant get several mails"
                      " in your first run.\nAfter the first run, the posts will be added to database"
                      " and you can turn notifications on.)")

                stat = input("Y/N: ").upper()

                # Checking Stat
                if (stat == "Y"):
                    stat = True
                elif (stat == "N"):
                    stat = False
                else:
                    print("\nWrong command. Try again.\n")
                    continue

                user_info = User_Database.User(user_mail,stat)

                #Adding user to database
                Mail.add_mail(user_info)

                print(user_mail,"successfully added to database.")


            try:
                url = "http://oyungezer.com.tr/haber"
                response = requests.get(url)
                html_content = response.content
                soup = BeautifulSoup(html_content, "html.parser")
            except Exception as e:
                print('An error occurred. Time: ' + str(datetime.strftime(datetime.now(),"%X")))
                continue

            link_html = soup.find_all("a")
            image_html = soup.find_all("img")

            ex_post_links = list()
            image_links = list()
            post_links = list()

            date = ""
            title = ""
            writer = ""
            item_text = ""

            for i in link_html:
                # Getting titles
                title = str(i['href'])
                if (title.startswith("/haber/")):
                    ex_post_links.append("http://oyungezer.com.tr" + title)

            for i in image_html:
                # Getting Images
                image = str(i['src'])
                if (image.startswith("/images/haberler/")):
                    image_links.append("http://oyungezer.com.tr" + image)

            for i, j in zip(ex_post_links, range(0, len(ex_post_links))):
                # Getting post links
                if (j % 2 == 0):
                    post_links.append(i)

            for link,picture,x in zip(post_links,image_links,range(0,3)):
                url = link
                response = requests.get(url)
                html_content = response.content
                soup = BeautifulSoup(html_content, "html.parser")

                date_html = soup.find_all("dd", {"class": "published"})
                title_html = soup.find_all("h2", {"itemprop": "headline"})
                writer_html = soup.find_all("span", {"class": "autor_name"})
                item_text_html = soup.find_all("div", {"class": "introtext"})

                for i in date_html:
                    date = str(i.text)
                    date = date.replace("\n", "")
                    date = date.replace("\t", "")

                for i in title_html:
                    title = str(i.text)
                    title = title.replace("\n", "")
                    title = title.replace("\t", "")

                for i in writer_html:
                    writer = str(i.text)
                    writer = writer.replace("\n", "")
                    writer = writer.replace("\t", "")

                for i in item_text_html:
                    item_text = str(i.text)
                    item_text = item_text.replace("\n", "")


                check_url = url.split("-")[0]
                #print(check_url)

                if (Post.check_if_post_exists(check_url)):

                    new_posts += 1
                    total_posts += 1
                    
                    #Adding post to database
                    new_post = Post_Database.Post(title,writer,date,item_text,url,picture)
                    Post.add_post(new_post)

                    #Text of mail
                    mail_text = new_post.text_of_mail()

                    #Getting mail addresses
                    address = Mail.get_mails()

                    #Sending mail to users
                    for mail in address:
                        Inform_User.send_mail(mail[0],mail_text)


            run_time += 1

            if (len(str(run_time)) == 1):
                run_time = "0" + str(run_time)

            if (new_posts == 0):
                text = "No post released. Time: "
            else:
                text = str(new_posts) + " post released. Time: "
            
            print(str(run_time) + ". run - " +  "Process finished. Waiting for 5 minutes. "
                  + text + str(datetime.strftime(datetime.now(),"%X")) + " - Today's number of posts: " + str(total_posts))

            run_time = int(run_time)
            
            time.sleep(300)


    elif (number.lower() == "q"):
        exit()

    else:
        print("Invalid command. Try again.")

