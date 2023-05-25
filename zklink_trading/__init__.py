#!/usr/bin/env python
# encoding: utf-8
import os
import click
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, request
from zklink_trading.settings import config
from flask_sqlalchemy import SQLAlchemy

from zklink_trading.blueprints.auth import auth_bp
from zklink_trading.blueprints.order import order_bp


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db = SQLAlchemy()


def create_app(config_name='testing'):
    app = Flask('zklink-trading')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_blueprints(app)
    register_commands(app)

    return app


def register_logging(app):
    class RequestFormatter(logging.Formatter):
        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/zklink-trading-demo.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(order_bp, url_prefix='/api/order')


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')
