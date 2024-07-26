from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Goal:
    db = "betterme_schema"

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.plan = data['plan']
        self.category = data['category']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.achieved = data['achieved']
        self.creater = None

    @classmethod
    def save_goal(cls, data):
        query = "INSERT INTO goals (title, plan, category, user_id, achieved) VALUES (%(title)s, %(plan)s, %(category)s, %(user_id)s, false)"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_all_goals(cls):
        query = "SELECT * FROM goals LEFT JOIN users ON users.id = goals.user_id;"
        results = connectToMySQL(cls.db).query_db(query)
        goals = []
        for goal in results:
            user_data = {
                "id": goal['user_id'],
                "first_name": goal['first_name']
            }
            this_goal = cls(goal)
            this_goal.creator = user_data
            goals.append(this_goal)
        return goals

    @classmethod
    def get_goals_by_id(cls, data):
        query = "SELECT * FROM goals LEFT JOIN users ON goals.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        goals = []
        for goal in results:
            this_goal = cls(goal)
            goals.append(this_goal)
        return goals

    @classmethod
    def get_goals_by_category(cls, data):
        query = "SELECT * FROM goals LEFT JOIN users ON goals.user_id = users.id WHERE users.id = %(user_id)s AND category = %(category)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        goals = []
        for goal in results:
            this_goal = cls(goal)
            goals.append(this_goal)
        return goals

    @classmethod
    def get_goal_by_id(cls, data):
        query = "SELECT * FROM goals WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) > 0:
            return cls(results[0])
        return None

    @classmethod
    def update_achieved(cls, data):
        query = "UPDATE goals SET achieved = %(achieved)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def edit_goal(cls, data):
        query = """
            UPDATE goals 
            SET title = %(title)s,
            plan = %(plan)s,
            category = %(category)s,
            achieved = %(achieved)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM goals WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_goal(data):
        is_valid = True
        if len(data['title']) < 3:
            is_valid = False
            flash("Title must be at least 3 characters.", "goal")
        if len(data['plan']) < 3:
            is_valid = False
            flash("Plan must be at least 3 characters.", "goal")
        if data['category'] == '':
            is_valid = False
            flash("Please input category.", "goal")
        return is_valid
