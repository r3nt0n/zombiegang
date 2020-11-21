#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n


from config import Config

from app.components import Logger, RemoteZession, Buffer, Proxy

#config = Config

logger = Logger(debug=Config.DEBUG)

#logger.set_level(logger.console_handler, 'DEBUG')
# logger.set_level(logger.console_handler, 'INFO')
# logger.set_level(logger.file_handler, 'DEBUG')

zession = RemoteZession()
buffer = Buffer()
proxy = Proxy()
#proxy.get_socks5_session('127.0.0.1', 9050)


def create_app():
    """
    Initialize the core application.
    """
    from flask import Flask, request
    app = Flask(__name__)
    app.config.from_object(Config)
    #app = Flask(__name__, instance_relative_config=False)
    #app.config.from_object('config.Config')

    logger.start()
    logger.log('starting app', level='DEBUG')

    # Initialize Plugins
    #db.init_app(app)
    #r.init_app(app)

    # log info after every request
    @app.after_request
    def after_request_func(response):
        logger.log('\r\n', 'DEBUG')
        logger.log('section: {}'.format(zession.current_section), 'QUESTION')
        logger.log('request: {}'.format(request), 'DEBUG')
        logger.log('form: {}'.format(request.form), 'DEBUG')
        return response


    with app.app_context():
        # Include our Routes
        from . import routes
        # Register Blueprints
        app.register_blueprint(routes.ajax_bp)
        app.register_blueprint(routes.login_bp)
        app.register_blueprint(routes.dashboard_bp)
        app.register_blueprint(routes.files_bp)
        app.register_blueprint(routes.logs_bp)
        app.register_blueprint(routes.members_bp)
        app.register_blueprint(routes.attacks_bp)

        return app
