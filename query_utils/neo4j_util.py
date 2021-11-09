#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from py2neo import Graph
from django.conf import settings

class neo4jUtil:
    def __init__(self):
        host = settings.NEO4J_CONNECTION["host"]
        user = settings.NEO4J_CONNECTION["user"]
        password = settings.NEO4J_CONNECTION["password"]
        self.driver = Graph(host, auth=(user, password))

    def run_cypher(self, cypher):
        result_list = self.driver.run(cypher).data()
        return result_list
