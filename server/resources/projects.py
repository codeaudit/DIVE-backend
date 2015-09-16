import os
import shutil

from flask import make_response, jsonify
from flask.ext.restful import Resource, reqparse

from .utilities import format_json

############################
# Projects
############################
projectsGetParser = reqparse.RequestParser()
projectsGetParser.add_argument('pID', type=str, default='')
projectsGetParser.add_argument('user_name', type=str, required=True)

projectsPostParser = reqparse.RequestParser()
projectsPostParser.add_argument('title', type=str, required=True)
projectsPostParser.add_argument('description', type=str, required=False)
projectsPostParser.add_argument('user_name', type=str, required=False)
projectsPostParser.add_argument('anonymous', type=bool, required=False, default=False)

projectsDeleteParser = reqparse.RequestParser()
projectsDeleteParser.add_argument('pID', type=str, default='')
class Projects(Resource):
    def get(self):
        args = projectsGetParser.parse_args()
        pID = args.get('pID').strip().strip('"')
        user_name = args.get('user_name')
        return MI.getProject(pID, user_name)

    # Create project, initialize directories and collections
    def post(self):
        args = projectsPostParser.parse_args()
        title = args.get('title')
        description = args.get('description')
        user_name = args.get('user_name')
        anonymous = args.get('anonymous')

        result = MI.postProject(title, description, user_name, anonymous)

        # If successful project creation
        if result[1] is 200:
            # Create data upload directory
            app.logger.info("Created upload directory for pID: %s", result[0]['pID'])
            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], result[0]['pID']))

        return result

    # Delete project and all associated data
    def delete(self):
        args = projectsDeleteParser.parse_args()
        pID = args.get('pID').strip().strip('"')
        print "DELETE", pID

        MI.deleteProject(pID)

        # Delete uploads directory
        shutil.rmtree(os.path.join(app.config['UPLOAD_FOLDER'], pID))
        return
