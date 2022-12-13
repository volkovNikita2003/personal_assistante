import sqlite3


db_budget_periods = [
    "day",
    "week",
    "month",
    "year",
    "all"
]


class DataBaseBudget:
    def __init__(self, db_file):
        self.connect = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connect.cursor()

    def _check_user(self, user_id):
        """Checks if the user is in the database"""

        result = self.cursor.execute(
            "SELECT `id` FROM `users` WHERE `user_id` = ?",
            (
                user_id,
            )
        )
        return bool(len(result.fetchall()))

    def add_user(self, user_id, sep=".", float_sep=","):
        """If the user is not in the database, then add"""

        if not self._check_user(user_id):
            self.cursor.execute(
                "INSERT INTO `users` (`user_id`, `sep`, `float_sep`) VALUES (?, ?, ?)",
                (
                    user_id,
                    sep,
                    float_sep,
                )
            )
            self.connect.commit()

    def update_sep(self, user_id, sep):
        """If the user is in the database, update its sep"""

        if self._check_user(user_id):
            self.cursor.execute(
                "UPDATE `users` SET `sep` = ? WHERE `user_id` = ?",
                (
                    sep,
                    user_id,
                )
            )
            self.connect.commit()

    def update_float_sep(self, user_id, float_sep):
        """If the user is in the database, update its float_sep"""

        if self._check_user(user_id):
            self.cursor.execute(
                "UPDATE `users` SET `float_sep` = ? WHERE `user_id` = ?",
                (
                    float_sep,
                    user_id,
                )
            )
        self.connect.commit()

    def get_user_sep(self, user_id):
        self.add_user(user_id)
        result = self.cursor.execute(
            "SELECT `sep` FROM `users` WHERE `user_id` = ?",
            (
                user_id,
            )
        )
        return result.fetchall()[0][0]

    def get_user_float_sep(self, user_id):
        self.add_user(user_id)
        result = self.cursor.execute(
            "SELECT `float_sep` FROM `users` WHERE `user_id` = ?",
            (
                user_id,
            )
        )
        return result.fetchall()[0][0]

    def get_user_seps(self, user_id):
        self.add_user(user_id)
        result = self.cursor.execute(
            "SELECT `sep`, `float_sep` FROM `users` WHERE `user_id` = ?",
            (
                user_id,
            )
        )
        return result.fetchall()[0]

    def add_revenue_record(self, user_id, summa, source=None, bank=None, account_type=None):
        """Creating a revenue record"""

        self.add_user(user_id)
        self.cursor.execute(
            "INSERT INTO `revenue` (`user_id`, `summa`, `source`, `bank`, `account_type`) VALUES (?, ?, ?, ?, ?)",
            (
                user_id,
                summa,
                source,
                bank,
                account_type,
            )
        )
        self.connect.commit()

    def add_expense_record(self, user_id, summa, title, category=None, counter=None, mass=None, bonus=None):
        """Creating a expense record"""

        self.add_user(user_id)
        self.cursor.execute(
            "INSERT INTO `expense` (`user_id`, `summa`, `title`, `category`, `counter`, `mass`, `bonus`) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                user_id,
                summa,
                title,
                category,
                counter,
                mass,
                bonus,
            )
        )
        self.connect.commit()

    def _get_records(self, table_name, user_id, period):
        """Get a story about revenue/expense"""

        date_filter = ""
        if period == db_budget_periods[0]:
            date_filter = " AND `date` BETWEEN datetime('now', '-1 days') AND datetime('now', 'localtime')"
        elif period == db_budget_periods[1]:
            date_filter = " AND `date` BETWEEN datetime('now', '-7 days') AND datetime('now', 'localtime')"
        elif period == db_budget_periods[2]:
            date_filter = " AND `date` BETWEEN datetime('now', '-30 days') AND datetime('now', 'localtime')"
        elif period == db_budget_periods[3]:
            date_filter = " AND `date` BETWEEN datetime('now', '-365 days') AND datetime('now', 'localtime')"

        result = self.cursor.execute(
            f"SELECT * FROM `{table_name}` WHERE `user_id` = ?{date_filter} ORDER BY `date`",
            (user_id,)
        )

        return result.fetchall()

    def get_revenue_records(self, user_id, period="all"):
        """Get a story about revenue"""
        table_name = "revenue"
        return self._get_records(table_name, user_id, period)

    def get_expense_records(self, user_id, period="all"):
        """Get a story about expense"""
        table_name = "expense"
        return self._get_records(table_name, user_id, period)

    def close(self):
        """Close the database connection"""
        self.connect.close()
