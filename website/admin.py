from flask_babel import gettext
import hedyweb
from website import statistics
from website.auth import requires_login, current_user, is_admin, pick
import utils
from flask import request
from flask_helpers import render_template


def routes(app, database):
    global DATABASE
    DATABASE = database

    @app.route('/admin', methods=['GET'])
    def get_admin_page():
        if not utils.is_testing_request(request) and not is_admin(current_user()):
            return utils.error_page(error=403, ui_message=gettext('unauthorized'))
        return render_template('admin/admin.html', page_title=gettext('title_admin'))

    @app.route('/admin/users', methods=['GET'])
    @requires_login
    def get_admin_users_page(user):
        if not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext('unauthorized'))

        category = request.args.get('filter', default=None, type=str)
        category = None if category == "null" else category

        substring = request.args.get('substring', default=None, type=str)
        start_date = request.args.get('start', default=None, type=str)
        end_date = request.args.get('end', default=None, type=str)
        language = request.args.get('language', default=None, type=str)
        keyword_language = request.args.get('keyword_language', default=None, type=str)

        substring = None if substring == "null" else substring
        start_date = None if start_date == "null" else start_date
        end_date = None if end_date == "null" else end_date
        language = None if language == "null" else language
        keyword_language = None if keyword_language == "null" else keyword_language

        if category:
            users = DATABASE.all_users(True)
        else:
            users = DATABASE.all_users(False)

        userdata = []
        fields = [
            'username', 'email', 'birth_year', 'country',
            'gender', 'created', 'last_login', 'verification_pending',
            'is_teacher', 'program_count', 'prog_experience', 'teacher_request',
            'experience_languages', 'language', 'keyword_language'
        ]

        for user in users:
            data = pick(user, *fields)
            data['email_verified'] = not bool(data['verification_pending'])
            data['is_teacher'] = bool(data['is_teacher'])
            data['teacher_request'] = True if data['teacher_request'] else None
            data['created'] = utils.timestamp_to_date(data['created'])
            data['last_login'] = utils.timestamp_to_date(data['last_login']) if data.get('last_login') else None
            if category == "language":
                if language != data['language']:
                    continue
            if category == "keyword_language":
                if keyword_language != data['keyword_language']:
                    continue
            if category == "username":
                if substring and substring not in data.get('username'):
                    continue
            if category == "email":
                if not data.get('email') or (substring and substring not in data.get('email')):
                    continue
            if category == "created":
                if start_date and utils.string_date_to_date(start_date) > data['created']:
                    continue
                if end_date and utils.string_date_to_date(end_date) < data['created']:
                    continue
            if category == "last_login":
                if not data.get('last_login'):
                    continue
                if start_date and utils.string_date_to_date(start_date) > data['last_login']:
                    continue
                if end_date and utils.string_date_to_date(end_date) < data['last_login']:
                    continue
            userdata.append(data)

        return render_template('admin/admin-users.html', users=userdata, page_title=gettext('title_admin'),
                               filter=category, start_date=start_date, end_date=end_date, email_filter=substring,
                               language_filter=language, keyword_language_filter=keyword_language)

    @app.route('/admin/classes', methods=['GET'])
    @requires_login
    def get_admin_classes_page(user):
        if not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext('unauthorized'))

        classes = [{
            "name": Class.get('name'),
            "teacher": Class.get('teacher'),
            "students": len(Class.get('students')) if 'students' in Class else 0,
            "stats": statistics.get_general_class_stats(Class.get('students', [])),
            "id": Class.get('id')
        } for Class in DATABASE.all_classes()]

        classes = sorted(classes, key=lambda d: d.get('stats').get('week').get('runs'), reverse=True)
        print(classes)

        return render_template('admin/admin-classes.html', classes=classes, page_title=gettext('title_admin'))

    @app.route('/admin/adventures', methods=['GET'])
    @requires_login
    def get_admin_adventures_page(user):
        if not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext('unauthorized'))

        all_adventures = sorted(DATABASE.all_adventures(), key=lambda d: d.get('date', 0), reverse=True)
        adventures = [{
            "id": adventure.get('id'),
            "creator": adventure.get('creator'),
            "name": adventure.get('name'),
            "level": adventure.get('level'),
            "public": "Yes" if adventure.get('public') else "No",
            "date": utils.localized_date_format(adventure.get('date'))
        } for adventure in all_adventures]


        return render_template('admin/admin-adventures.html', adventures=adventures, page_title=gettext('title_admin'))

    @app.route('/admin/stats', methods=['GET'])
    @requires_login
    def get_admin_stats_page(user):
        if not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext('unauthorized'))
        return render_template('admin/admin-stats.html', page_title=gettext('title_admin'))

    @app.route('/admin/logs', methods=['GET'])
    @requires_login
    def get_admin_logs_page(user):
        if not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext('unauthorized'))
        return render_template('admin/admin-logs.html', page_title=gettext('title_admin'))


    @app.route('/admin/achievements', methods=['GET'])
    @requires_login
    def get_admin_achievements_page(user):
        if not is_admin(user):
            return utils.error_page(error=403, ui_message=gettext('unauthorized'))

        stats = {}
        achievements = hedyweb.AchievementTranslations().get_translations("en").get("achievements")
        for achievement in achievements.keys():
            stats[achievement] = {}
            stats[achievement]["name"] = achievements.get(achievement).get("title")
            stats[achievement]["description"] = achievements.get(achievement).get("text")
            stats[achievement]["count"] = 0

        user_achievements = DATABASE.get_all_achievements()
        total = len(user_achievements)
        for user in user_achievements:
            for achieved in user.get("achieved", []):
                stats[achieved]["count"] += 1

        return render_template('admin/admin-achievements.html', stats=stats,
                               total=total, page_title=gettext('title_admin'))

