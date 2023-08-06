import os
import json

from bravado.requests_client import RequestsClient
from bravado.client import SwaggerClient
from bravado.swagger_model import load_file
from simplejson import JSONDecodeError

from .models import Project, MapToken, Analysis
from .exceptions import RefreshTokenException
from .utils import mkdir_p

SPEC_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         'spec.yml')


class API(object):
    """Class to interact with Raster Foundry API"""

    def __init__(self, refresh_token=None, api_token=None,
                 host='app.rasterfoundry.com', scheme='https'):
        """Instantiate an API object to make requests to Raster Foundry's REST API

        Args:
            refresh_token (str): optional token used to obtain an API token to
                                 make API requests
            api_token (str): optional token used to authenticate API requests
            host (str): optional host to use to make API requests against
            scheme (str): optional scheme to override making requests with
        """

        self.http = RequestsClient()
        self.scheme = scheme

        spec = load_file(SPEC_PATH)

        spec['host'] = host
        spec['schemes'] = [scheme]

        split_host = host.split('.')
        split_host[0] = 'tiles'
        self.tile_host = '.'.join(split_host)

        config = {'validate_responses': False}
        self.client = SwaggerClient.from_spec(spec, http_client=self.http,
                                              config=config)

        if refresh_token and not api_token:
            api_token = self.get_api_token(refresh_token)
        elif not api_token:
            raise Exception('Must provide either a refresh token or API token')

        self.api_token = api_token
        self.http.session.headers['Authorization'] = 'Bearer {}'.format(
            api_token)

    def get_api_token(self, refresh_token):
        """Retrieve API token given a refresh token

        Args:
            refresh_token (str): refresh token used to make a request for a new
                                 API token

        Returns:
            str
        """
        post_body = {'refresh_token': refresh_token}

        try:
            response = self.client.Authentication.post_tokens(
                refreshToken=post_body).future.result()
            return response.json()['id_token']
        except JSONDecodeError:
            raise RefreshTokenException('Error using refresh token, please '
                                        'verify it is valid')

    @property
    def map_tokens(self):
        """List map tokens a user has access to

        Returns:
            List[MapToken]
        """

        has_next = True
        page = 0
        map_tokens = []
        while has_next:
            paginated_map_tokens = (
                self.client.Imagery.get_map_tokens(page=page).result()
            )
            map_tokens += [
                MapToken(map_token, self)
                for map_token in paginated_map_tokens.results
            ]
            page = paginated_map_tokens.page + 1
            has_next = paginated_map_tokens.hasNext
        return map_tokens

    @property
    def projects(self):
        """List projects a user has access to

        Returns:
            List[Project]
        """
        has_next = True
        projects = []
        page = 0
        while has_next:
            paginated_projects = self.client.Imagery.get_projects(
                page=page).result()
            has_next = paginated_projects.hasNext
            page = paginated_projects.page + 1
            for project in paginated_projects.results:
                projects.append(Project(project, self))
        return projects

    @property
    def analyses(self):
        """List analyses a user has access to

        Returns:
            List[Analysis]
        """
        has_next = True
        analyses = []
        page = 0
        while has_next:
            paginated_analyses = self.client.Lab.get_tool_runs(page=page).result()
            has_next = paginated_analyses.hasNext
            page = paginated_analyses.page + 1
            for analysis in paginated_analyses.results:
                analyses.append(Analysis(analysis, self))
        return analyses

    def get_datasources(self, **kwargs):
        return self.client.Datasources.get_datasources(**kwargs).result()

    def get_scenes(self, **kwargs):
        bbox = kwargs.get('bbox')
        if bbox and hasattr(bbox, 'bounds'):
            kwargs['bbox'] = ','.join(str(x) for x in bbox.bounds)
        elif bbox and type(bbox) != type(','.join(str(x) for x in bbox)): # NOQA
            kwargs['bbox'] = ','.join(str(x) for x in bbox)
        return self.client.Imagery.get_scenes(**kwargs).result()

    def get_project_configs(self, project_ids, annotation_uris):
        """Get data needed to create project config file for prep_train_data

        The prep_train_data script requires a project config files which
        lists the images and annotation URIs associated with each project
        that will be used to generate training data.

        Args:
            project_ids: list of project ids to make training data from
            annotation_uris: list of corresponding annotation URIs

        Returns:
            Object of form [{'images': [...], 'annotations':...}, ...]
        """
        project_configs = []
        for project_id, annotation_uri in zip(project_ids, annotation_uris):
            proj = Project(
                self.client.Imagery.get_projects_uuid(uuid=project_id).result(),
                self)
            image_uris = proj.get_image_source_uris()
            project_configs.append({
                'id': project_id,
                'images': image_uris,
                'annotations': annotation_uri
            })

        return project_configs

    def write_project_configs(self, project_ids, annotation_uris, output_path):
        """Write project config file to disk.

        This file is needed by Raster Vision to prepare training data, make
        predictions, and evaluate predictions.

        Args:
            project_ids: list of project ids to make training data from
            annotation_uris: list of corresponding annotation URIs
            output_path: where to write the project config file
        """
        project_configs = self.get_project_configs(
            project_ids, annotation_uris)
        mkdir_p(os.path.dirname(output_path))
        with open(output_path, 'w') as output_file:
            json.dump(project_configs, output_file, sort_keys=True, indent=4)
