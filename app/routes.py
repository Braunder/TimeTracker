# Импорт необходимых модулей
from flask import jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_restx import Resource, fields, Namespace
from app import db
from app.models import User, Project, TimeEntry
from app.schemas import UserSchema, ProjectSchema, TimeEntrySchema, ReportParamsSchema
from datetime import datetime
from sqlalchemy import func
from marshmallow import ValidationError

# Создание namespace для API документации
ns = Namespace('api', description='API операции')

# Модели для Swagger документации
user_model = ns.model('User', {
    'id': fields.Integer(readonly=True),
    'username': fields.String(required=True, description='Имя пользователя'),
    'email': fields.String(required=True, description='Email пользователя'),
    'password': fields.String(required=True, description='Пароль пользователя'),
    'is_manager': fields.Boolean(default=False, description='Является ли пользователь менеджером')
})

project_model = ns.model('Project', {
    'id': fields.Integer(readonly=True, description='ID проекта'),
    'name': fields.String(required=True, description='Название проекта'),
    'description': fields.String(description='Описание проекта')
})

time_entry_model = ns.model('TimeEntry', {
    'id': fields.Integer(readonly=True, description='ID записи времени'),
    'project_id': fields.Integer(required=True, description='ID проекта'),
    'date': fields.Date(required=True, description='Дата записи'),
    'hours': fields.Float(required=True, description='Количество часов')
})

login_model = ns.model('Login', {
    'username': fields.String(required=True, description='Имя пользователя'),
    'password': fields.String(required=True, description='Пароль')
})

report_model = ns.model('Report', {
    'id': fields.Integer(description='ID пользователя'),
    'hours': fields.Float(description='Количество часов')
})

# Инициализация схем
user_schema = UserSchema()
project_schema = ProjectSchema()
time_entry_schema = TimeEntrySchema()
report_params_schema = ReportParamsSchema()

# Ресурсы API
@ns.route('/auth/register')
class Register(Resource):
    @ns.expect(user_model)
    @ns.response(201, 'User created successfully')
    @ns.response(400, 'Validation error')
    def post(self):
        """Регистрация нового пользователя"""
        try:
            data = user_schema.load(self.api.payload)
            if User.query.filter_by(username=data['username']).first():
                return {'error': 'Username already exists'}, 400
            
            user = User(
                username=data['username'],
                email=data['email'],
                is_manager=data.get('is_manager', False)
            )
            user.set_password(data['password'])
            
            db.session.add(user)
            db.session.commit()
            
            return {'message': 'User created successfully'}, 201
        except ValidationError as e:
            return {'error': e.messages}, 400

@ns.route('/auth/login')
class Login(Resource):
    @ns.expect(login_model)
    @ns.response(200, 'Login successful')
    @ns.response(401, 'Invalid credentials')
    def post(self):
        """Вход пользователя и получение токена"""
        try:
            data = self.api.payload
            user = User.query.filter_by(username=data['username']).first()
            
            if user and user.check_password(data['password']):
                access_token = create_access_token(identity=user.id)
                return {'access_token': access_token}, 200
            
            return {'error': 'Invalid credentials'}, 401
        except Exception as e:
            return {'error': str(e)}, 400

@ns.route('/projects')
class ProjectList(Resource):
    @ns.doc(security='Bearer')
    @ns.marshal_list_with(project_model)
    @jwt_required()
    def get(self):
        """Получение списка всех проектов"""
        projects = Project.query.all()
        return projects

    @ns.doc(security='Bearer')
    @ns.expect(project_model)
    @ns.marshal_with(project_model, code=201)
    @jwt_required()
    def post(self):
        """Создание нового проекта"""
        try:
            data = project_schema.load(self.api.payload)
            project = Project(**data)
            db.session.add(project)
            db.session.commit()
            return project, 201
        except ValidationError as e:
            return {'error': e.messages}, 400

@ns.route('/projects/<int:id>')
class ProjectResource(Resource):
    @ns.doc(security='Bearer')
    @ns.marshal_with(project_model)
    @jwt_required()
    def get(self, id):
        """Получение проекта по ID"""
        project = Project.query.get_or_404(id)
        return project

    @ns.doc(security='Bearer')
    @ns.expect(project_model)
    @ns.marshal_with(project_model)
    @jwt_required()
    def put(self, id):
        """Обновление проекта"""
        try:
            project = Project.query.get_or_404(id)
            data = project_schema.load(self.api.payload)
            for key, value in data.items():
                setattr(project, key, value)
            db.session.commit()
            return project
        except ValidationError as e:
            return {'error': e.messages}, 400

    @ns.doc(security='Bearer')
    @ns.response(204, 'Project deleted')
    @jwt_required()
    def delete(self, id):
        """Удаление проекта"""
        project = Project.query.get_or_404(id)
        db.session.delete(project)
        db.session.commit()
        return '', 204

@ns.route('/time-entries')
class TimeEntryList(Resource):
    @ns.doc(security='Bearer')
    @ns.marshal_list_with(time_entry_model)
    @jwt_required()
    def get(self):
        """Получение записей о времени пользователя"""
        user_id = get_jwt_identity()
        time_entries = TimeEntry.query.filter_by(user_id=user_id).all()
        return time_entries

    @ns.doc(security='Bearer')
    @ns.expect(time_entry_model)
    @ns.marshal_with(time_entry_model, code=201)
    @jwt_required()
    def post(self):
        """Создание новой записи о времени"""
        try:
            data = time_entry_schema.load(self.api.payload)
            data['user_id'] = get_jwt_identity()
            time_entry = TimeEntry(**data)
            db.session.add(time_entry)
            db.session.commit()
            return time_entry, 201
        except ValidationError as e:
            return {'error': e.messages}, 400

@ns.route('/time-entries/<int:id>')
class TimeEntryResource(Resource):
    @ns.doc(security='Bearer')
    @ns.marshal_with(time_entry_model)
    @jwt_required()
    def get(self, id):
        """Получение записи о времени по ID"""
        user_id = get_jwt_identity()
        time_entry = TimeEntry.query.filter_by(id=id, user_id=user_id).first_or_404()
        return time_entry

    @ns.doc(security='Bearer')
    @ns.expect(time_entry_model)
    @ns.marshal_with(time_entry_model)
    @jwt_required()
    def put(self, id):
        """Обновление записи о времени"""
        try:
            user_id = get_jwt_identity()
            time_entry = TimeEntry.query.filter_by(id=id, user_id=user_id).first_or_404()
            data = time_entry_schema.load(self.api.payload)
            for key, value in data.items():
                setattr(time_entry, key, value)
            db.session.commit()
            return time_entry
        except ValidationError as e:
            return {'error': e.messages}, 400

    @ns.doc(security='Bearer')
    @ns.response(204, 'Time entry deleted')
    @jwt_required()
    def delete(self, id):
        """Удаление записи о времени"""
        user_id = get_jwt_identity()
        time_entry = TimeEntry.query.filter_by(id=id, user_id=user_id).first_or_404()
        db.session.delete(time_entry)
        db.session.commit()
        return '', 204

@ns.route('/reports/project/<int:project_id>')
class ProjectReport(Resource):
    @ns.doc(security='Bearer')
    @ns.param('start_date', 'Start date (YYYY-MM-DD)')
    @ns.param('end_date', 'End date (YYYY-MM-DD)')
    @ns.marshal_list_with(report_model)
    @jwt_required()
    def get(self, project_id):
        """Получение отчета по проекту за период (только для менеджеров)"""
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        if not user.is_manager:
            return {'error': 'Only managers can access reports'}, 403
        
        try:
            params = report_params_schema.load(self.api.payload or {})
            report = db.session.query(
                TimeEntry.user_id,
                func.sum(TimeEntry.hours).label('hours')
            ).filter(
                TimeEntry.project_id == project_id,
                TimeEntry.date >= params['start_date'],
                TimeEntry.date < params['end_date']
            ).group_by(TimeEntry.user_id).all()
            
            return [{
                'id': r.user_id,
                'hours': float(r.hours)
            } for r in report]
        except ValidationError as e:
            return {'error': e.messages}, 400 