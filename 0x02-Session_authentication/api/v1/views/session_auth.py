#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from api.v1.app import auth


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ DELETE /api/v1/auth_session/logout
    destroy user's session
    """
    destroyed = auth.destroy_session(request)
    if destroyed:
        return jsonify({})
    else:
        abort(404)
