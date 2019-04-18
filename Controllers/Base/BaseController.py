from flask import Flask, request, jsonify


def http_response(obj):
    return jsonify(obj)
