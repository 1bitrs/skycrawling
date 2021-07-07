from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from skywalking import agent, config


server = Flask(__name__)
server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/skycrawling?charset:utf8mb4'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
server.config['SW_AGENT_COLLECTOR_BACKEND_SERVICES'] = '127.0.0.1:11800'
server.config['SW_AGENT_PROTOCOL'] = 'http'
server.config['SW_AGENT_INSTANCE'] = 'skycrawling'
db: SQLAlchemy = SQLAlchemy(server)

config.init(collector='127.0.0.1:11800', service='skycrawling')
config.disable_plugins = ['sw_aiohttp', 'sw_django', 'sw_elasticsearch', 
                          'sw_kafka', 'sw_pymongo', 'sw_pyramid', 
                          'sw_rabbitmq', 'sw_redis', 'sw_sanic', 
                          'sw_tornado', 'sw_aiohttp', 'sw_django', 
                          'sw_elasticsearch', 'sw_kafka', 'sw_pymongo', 
                          'sw_pyramid', 'sw_rabbitmq', 'sw_redis', 
                          'sw_sanic', 'sw_tornado',]
agent.start()
