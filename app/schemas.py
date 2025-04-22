from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    # Схема для валидации данных пользователя
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    is_manager = fields.Bool(required=False, default=False)

class ProjectSchema(Schema):
    # Схема для валидации данных проекта
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(required=False)

class TimeEntrySchema(Schema):
    # Схема для валидации данных записи времени
    project_id = fields.Int(required=True)
    date = fields.Date(required=True)
    hours = fields.Float(required=True, validate=validate.Range(min=0, max=24))

class ReportParamsSchema(Schema):
    # Схема для валидации параметров отчета
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True) 