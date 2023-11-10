import database
from auth import get_current_username
from datetime import datetime, timedelta



class Notifications:
    def __init__(self, current_username, user_id, db):
        self.username = current_username
        self.db = db
        self.user_id = user_id

    def __pending_requests_notif(self):
        pending_requests = self.db.get_pending_requests(get_current_username())
        if pending_requests:
            print("----------------------------------")
            print(
                "[Notification] - You have "
                + str(len(pending_requests))
                + " pending friend request(s). Go to the 'Friend Requests' tab to accept/reject."
            )
            print("----------------------------------\n")

    def __unread_messages_notif(self):
        unread_messages = self.db.get_unread_messages(self.user_id)
        if unread_messages:
            print("----------------------------------")
            print(
                "[Notification] - You have "
                + str(len(unread_messages))
                + " unread message(s). Go to the 'Messages' tab."
            )
            print("----------------------------------\n")

    def __student_joined_notif(self):
        new_students = self.db.get_student_who_joined_for_notification(self.user_id)
        if new_students:
            print("[Notification] - New students in InCollege:")
            for student in new_students:
                print(f"\tStudent {student[0].capitalize()} {student[1].capitalize()} has joined InCollege!")

    def __is_within_last_seven_days(self, dt):
        now = datetime.now()
        seven_days_ago = now - timedelta(days=7)
        return seven_days_ago <= dt <= now

    def __not_applied_for_a_job_notif(self):
        times = self.db.get_time_of_job_applications(self.user_id)
        has_applied_in_past_seven_days = False
        for time in times:
            print("debug time", time)
        # if self.__is_within_last_seven_days(time):
        #    has_applied_in_past_seven_days = True
        if not has_applied_in_past_seven_days:
            print("----------------------------------")
            print(
                "[Notification] - Remember - you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!"
            )
            print("----------------------------------\n")

    def show_notifications(self):
        self.__pending_requests_notif()
        self.__unread_messages_notif()
        self.__student_joined_notif()
        self.__not_applied_for_a_job_notif()
