# -*- coding: utf-8 -*-

import os.path
from collections import OrderedDict
from datetime import datetime
from distutils.version import LooseVersion
from utilities import path
from utilities import checks
from utilities import helpers
from utilities import PROJECT_DIR, DEFAULT_TEMPLATE_PROJECT
from utilities import CONTAINERS_YAML_DIRNAME
from utilities import configuration
from utilities.globals import mem
from utilities.time import date_from_string
from controller import __version__
from controller import project
from controller import gitter
from controller import COMPOSE_ENVIRONMENT_FILE, PLACEHOLDER
from controller import SUBMODULES_DIR, RAPYDO_CONFS, RAPYDO_GITHUB
from controller.builds import locate_builds
from controller.dockerizing import Dock
from controller.compose import Compose
from controller.scaffold import EndpointScaffold
from controller.configuration import read_yamls
from utilities.logs import get_logger, suppress_stdout

log = get_logger(__name__)

# FIXME: move somewhere
STATUS_RELEASED = "released"
STATUS_DISCONTINUED = "discontinued"
STATUS_DEVELOPING = "developing"


class Application(object):

    """
    ## Main application class

    It handles all implemented commands,
    which were defined in `argparser.yaml`
    """

    def __init__(self, arguments):
        self.arguments = arguments
        self.current_args = self.arguments.current_args
        self.reserved_project_names = self.get_reserved_project_names()

        self.run()

    def get_args(self):

        # Action
        self.action = self.current_args.get('action')
        mem.action = self.action
        if self.action is None:
            log.exit("Internal misconfiguration")
        else:
            log.info("Do request: %s" % self.action)

        # Action aliases
        self.initialize = self.action == 'init'
        self.update = self.action == 'update'
        self.upgrade = self.action == 'upgrade'
        self.check = self.action == 'check'

        # Others
        self.is_template = False
        self.tested_connection = False
        self.project = self.current_args.get('project')
        self.rapydo_version = None  # To be retrieved from projet_configuration
        self.version = None
        self.releases = {}
        self.gits = {}

        if self.project is not None:
            if "_" in self.project:
                suggest = "\nPlease consider to rename %s into %s" % (
                    self.project, self.project.replace("_", "")
                )
                log.exit(
                    "Wrong project name, _ is not a valid character. %s" %
                    suggest
                )

            if self.project in self.reserved_project_names:
                log.exit(
                    "You selected a reserved name, invalid project name: %s"
                    % self.project
                )

        self.development = self.current_args.get('development')

    def check_projects(self):

        try:
            projects = helpers.list_path(PROJECT_DIR)
        except FileNotFoundError:
            log.exit("Could not access the dir '%s'" % PROJECT_DIR)

        if self.project is None:
            prj_num = len(projects)

            if prj_num == 0:
                log.exit(
                    "No project found (%s folder is empty?)"
                    % PROJECT_DIR
                )
            elif prj_num > 1:
                log.exit(
                    "Please select the --project option on one " +
                    "of the following:\n\n %s\n" % projects)
            else:
                # make it the default
                self.project = projects.pop()
                self.current_args['project'] = self.project
        else:
            if self.project not in projects:
                log.exit(
                    "Wrong project '%s'.\n" % self.project +
                    "Select one of the following:\n\n %s\n" % projects)

        log.checked("Selected project: %s" % self.project)

        self.is_template = self.project == DEFAULT_TEMPLATE_PROJECT

    def check_installed_software(self):

        # Check if docker is installed
        self.check_program('docker', min_version="1.13")
        # Use it
        self.docker = Dock()

        # Check docker-compose version
        self.check_python_package('compose', min_version="1.18")
        # self.check_python_package('docker', min_version="2.4.2")
        self.check_python_package('docker', min_version="2.6.1")
        self.check_python_package(
            'utilities', min_version=__version__, max_version=__version__)

        # Check if git is installed
        self.check_program('git')  # , max_version='2.14.3')

    def check_program(self, program, min_version=None, max_version=None):
        found_version = checks.executable(executable=program)
        if found_version is None:
            log.exit(
                "Missing requirement.\n" +
                "Please make sure that '%s' is installed" % program
            )

        if min_version is not None:
            if LooseVersion(min_version) > LooseVersion(found_version):
                version_error = "Minimum supported version for %s is %s" \
                    % (program, min_version)
                version_error += ", found %s " % (found_version)
                log.exit(version_error)

        if max_version is not None:
            if LooseVersion(max_version) < LooseVersion(found_version):
                version_error = "Maximum supported version for %s is %s" \
                    % (program, max_version)
                version_error += ", found %s " % (found_version)
                log.exit(version_error)

        log.checked("%s version: %s" % (program, found_version))

    def check_python_package(
            self, package, min_version=None, max_version=None):

        found_version = checks.package(package)
        if found_version is None:
            log.exit(
                "Could not find the following python package: %s" % package)

        if min_version is not None:
            if LooseVersion(min_version) > LooseVersion(found_version):
                version_error = "Minimum supported version for %s is %s" \
                    % (package, min_version)
                version_error += ", found %s " % (found_version)
                log.exit(version_error)

        if max_version is not None:
            if LooseVersion(max_version) < LooseVersion(found_version):
                version_error = "Maximum supported version for %s is %s" \
                    % (package, max_version)
                version_error += ", found %s " % (found_version)
                log.exit(version_error)

        log.checked("%s version: %s" % (package, found_version))

    def inspect_main_folder(self):
        """
        Since the rapydo command only works on rapydo-core or a rapydo fork
        we want to ensure that the current folder have a structure rapydo-like
        This check is only based on file existence.
        Further checks are performed later in the following steps
        """

        if gitter.get_local(".") is None:
            log.exit(
                """You are not in a git repository
\nPlease note that this command only works from inside a rapydo-like repository
Verify that you are in the right folder, now you are in: %s
                """ % (os.getcwd())
            )

        # FIXME: move in a project_defaults.yaml?
        required_files = [
            PROJECT_DIR,
            'data',
            'projects',
            'submodules'
        ]

        obsolete_files = [
            'confs',
            'confs/backend.yml',
            'confs/frontend.yml',  # it is optional, but we expect to find it
        ]

        for fname in required_files:
            if not os.path.exists(fname):

                extra = ""

                if fname == 'data':
                    extra = """
\nPlease also note that the data dir is not automatically created,
if you are in the right repository consider to create it by hand
"""

                log.exit(
                    """File or folder not found %s
\nPlease note that this command only works from inside a rapydo-like repository
Verify that you are in the right folder, now you are in: %s%s
                    """ % (fname, os.getcwd(), extra)
                )

        for fname in obsolete_files:
            if os.path.exists(fname):
                log.exit(
                    "Project %s contains an obsolete file or folder: %s",
                    self.project, fname
                )

    def inspect_project_folder(self):

        # FIXME: move in a project_defaults.yaml?
        required_files = [
            'confs',
            'backend',
            'backend/apis',
            'backend/models',
            'backend/swagger',
            'backend/tests',
        ]
        obsolete_files = [
            'backend/__main__.py'
        ]

        if self.frontend:
            required_files.extend(
                [
                    'frontend',
                    'frontend/js',
                    'frontend/templates',
                    'frontend/bower.json',
                ]
            )
        for fname in required_files:
            fpath = os.path.join(PROJECT_DIR, self.project, fname)
            if not os.path.exists(fpath):
                log.exit(
                    """Project %s is invalid: file or folder not found %s
                    """ % (self.project, fpath)
                )

        for fname in obsolete_files:
            fpath = os.path.join(PROJECT_DIR, self.project, fname)
            if os.path.exists(fpath):
                log.exit(
                    "Project %s contains an obsolete file or folder: %s",
                    self.project, fpath
                )

    def read_specs(self):
        """ Read project configuration """

        default_file_path = os.path.join(SUBMODULES_DIR, RAPYDO_CONFS)
        project_file_path = helpers.project_dir(self.project)
        self.specs = configuration.read(
            default_file_path,
            project_path=project_file_path,
            is_template=self.is_template
        )

        self.vars = self.specs.get('variables', {})
        log.checked("Loaded containers configuration")

        self.frontend = self.vars \
            .get('frontend', {}) \
            .get('enable', False)
        log.very_verbose("Frontend is %s" % self.frontend)

        # Your project version
        self.version = self.specs.get('project', {}).get('version', None)

        # Check if project supports releases
        self.releases = self.specs.get('releases', {})
        if len(self.releases) > 0:
            log.verbose("Your project supports releases")

            # Check if the current version is listed in releases
            if self.version not in self.releases:
                log.exit(
                    "Releases misconfiguration: "+
                    "current version (%s) not found" % self.version
                )
            current_release = self.releases.get(self.version)
            self.rapydo_version = current_release.get("rapydo")

            # rapydo version is mandatory
            if self.rapydo_version is None:
                log.exit(
                    "Releases misconfiguration: "+
                    "missing rapydo version in release %s" % self.version
                )

        # If your project does not support releases, you can specify
        # rapydo version in the project block
        rapydo_version = self.specs.get('project', {}).get('rapydo', None)
        if self.rapydo_version is None:
            self.rapydo = rapydo_version

        # You specified a rapydo version both in project and releases
        elif rapydo_version is not None:

            if rapydo_version == self.rapydo_version:
                log.warning(
                    "You specified rapydo version in both project and release")
            else:
                err = "Rapydo version mismatch. "
                err += "You specified %s in project" % rapydo_version
                err += " and %s in current release." % self.rapydo_version
                err += "\nYou should remove such information from project"
                log.exit(err)

    def verify_rapydo_version(self, do_exit=True):
        """
        If your project requires a specific rapydo version, check if you are
        the rapydo-controller matching that version
        """
        if self.rapydo_version is None:
            return True

        r = LooseVersion(self.rapydo_version)
        c = LooseVersion(__version__)
        if r == c:
            return True

        if r > c:
            action = "Upgrade your controller to version %s" % r
        else:
            action = "Downgrade your controller to version %s" % r
            action += " or upgrade your project"

        exit_message = "This project requires rapydo-controller %s" % r
        exit_message += ", you are using %s" % c
        exit_message += "\n\n%s\n" % action

        if do_exit:
            log.exit(exit_message)
        else:
            log.warning(exit_message)

        return False

    def verify_connected(self):
        """ Check if connected to internet """

        connected = checks.internet_connection_available()
        if not connected:
            log.exit('Internet connection unavailable')
        else:
            log.checked("Internet connection available")
            self.tested_connection = True
        return

    def working_clone(self, name, repo, confs_only=False):

        # substitute values starting with '$$'
        if confs_only:
            myvars = {}
        else:
            myvars = {
                'frontend': self.frontend,
                'devel': self.development,
            }
        repo = project.apply_variables(repo, myvars)

        # Is this single repo enabled?
        repo_enabled = repo.pop('if', False)
        if not repo_enabled:
            return

        if self.upgrade and self.current_args.get('current'):
            repo['do'] = True
        else:
            repo['do'] = self.initialize

        # This step may require an internet connection in case of 'init'
        if not self.tested_connection and self.initialize:
            self.verify_connected()

        ################
        # - repo path to the repo name
        if 'path' not in repo:
            repo['path'] = name
        # - version is the one we have on the working controller
        if 'branch' not in repo:
            if confs_only or self.rapydo_version is None:
                repo['branch'] = __version__
            else:
                repo['branch'] = self.rapydo_version

        return gitter.clone(**repo)

    def git_submodules(self, confs_only=False):
        """ Check and/or clone git projects """

        if confs_only:
            repos = {}
            repos[RAPYDO_CONFS] = {
                "online_url": "%s/%s.git" % (RAPYDO_GITHUB, RAPYDO_CONFS),
                "if": "true"
            }
        else:
            repos = self.vars.get('repos').copy()
        # core_url = core.get('online_url')

        self.gits['main'] = gitter.get_repo(".")

        # is_core = gitter.compare_repository(
        #     local, None, core_url, check_only=True)

        # if is_core:
        #     log.info("You are working on rapydo-core, not a fork")
        #     gits['main'] = local
        # else:
        #     core_path = core.get('path')
        #     if core_path is None:
        #         core_path = core_key
        #     gits['main'] = gitter.upstream(
        #         url=core_url, path=core_path, do=self.initialize)

        for name, repo in repos.items():
            self.gits[name] = self.working_clone(
                name, repo, confs_only=confs_only)

    def git_update_repos(self):

        for name, gitobj in self.gits.items():
            if gitobj is not None:
                gitter.update(name, gitobj)

    def prepare_composers(self):

        confs = self.vars.get('composers', {})

        # substitute values starting with '$$'
        myvars = {
            'frontend': self.frontend,
            'logging': self.current_args.get('collect_logs'),
            'devel': self.development,
            'mode': self.current_args.get('mode'),
            'baseconf': helpers.current_dir(
                SUBMODULES_DIR, RAPYDO_CONFS, CONTAINERS_YAML_DIRNAME
            ),
            'customconf': helpers.project_dir(
                self.project,
                CONTAINERS_YAML_DIRNAME
            )
        }
        compose_files = OrderedDict()
        for name, conf in confs.items():
            compose_files[name] = project.apply_variables(conf, myvars)
        return compose_files

    def read_composers(self):

        # Find configuration that tells us which files have to be read
        compose_files = self.prepare_composers()

        # Read necessary files
        self.services, self.files, self.base_services, self.base_files = \
            read_yamls(compose_files)
        log.verbose("Configuration order:\n%s" % self.files)

    def build_dependencies(self):
        """ Look up for builds which are depending on templates """

        if self.action == 'shell' \
           or self.action == 'template' \
           or self.action == 'coveralls' \
           or self.action == 'ssl-dhparam':
            return

        # TODO: check all builds against their Dockefile latest commit
        # log.pp(self.services)

        # Compare builds depending on templates
        # NOTE: slow operation!
        self.builds, self.template_builds, overriding_imgs = locate_builds(
            self.base_services, self.services)

        dimages = self.docker.images()

        if not self.current_args.get('rebuild_templates', False):
            self.verify_template_builds(
                dimages, self.template_builds)

        if self.action in ['check', 'init', 'update']:
            self.verify_obsolete_builds(
                dimages, self.builds, overriding_imgs, self.template_builds)

    def get_build_timestamp(self, timestamp, as_date=False):

        if timestamp is None:
            log.warning("Received a null timestamp, defaulting to zero")
            timestamp = 0
        # Prior of dockerpy 2.5.1 image build timestamps were given as epoch
        # i.e. were convertable to float
        # From dockerpy 2.5.1 we are obtained strings like this:
        # 2017-09-22T07:10:35.822772835Z as we need to convert to epoch
        try:
            # verify if timestamp is already an epoch
            float(timestamp)
        except ValueError:
            # otherwise, convert it
            timestamp = date_from_string(timestamp).timestamp()

        if as_date:
            return datetime.fromtimestamp(timestamp)
        return timestamp

    def build_is_obsolete(self, build):
        # compare dates between git and docker
        path = build.get('path')
        Dockerfile = os.path.join(path, 'Dockerfile')

        build_templates = self.gits.get('build-templates')
        vanilla = self.gits.get('main')

        if path.startswith(build_templates.working_dir):
            git_repo = build_templates
        elif path.startswith(vanilla.working_dir):
            git_repo = vanilla
        else:
            log.exit("Unable to find git repo containing %s" % Dockerfile)

        obsolete, build_ts, last_commit = gitter.check_file_younger_than(
            gitobj=git_repo,
            filename=Dockerfile,
            timestamp=self.get_build_timestamp(build.get('timestamp'))
        )

        return obsolete, build_ts, last_commit

    def verify_template_builds(self, docker_images, builds):

        if len(builds) == 0:
            log.debug("No template build to be verified")
            return

        found_obsolete = 0
        fmt = "%Y-%m-%d %H:%M:%S"
        for image_tag, build in builds.items():

            if image_tag not in docker_images:

                found_obsolete += 1
                message = "Missing template build for %s (%s)" % (
                    build['service'], image_tag)
                if self.action == 'check':
                    message += "\nSuggestion: execute the init command"
                    log.exit(message)
                else:
                    log.debug(message)
                    dc = Compose(files=self.base_files)
                    dc.build_images(
                        builds={image_tag: build}, current_version=__version__)

                continue

            obsolete, build_ts, last_commit = self.build_is_obsolete(build)
            if obsolete:
                found_obsolete += 1
                b = datetime.fromtimestamp(build_ts).strftime(fmt)
                c = last_commit.strftime(fmt)
                message = "Template image %s is obsolete" % image_tag
                message += " (built on %s" % b
                message += " but changed on %s)" % c
                if self.current_args.get('rebuild'):
                    log.info("%s, rebuilding", message)
                    dc = Compose(files=self.base_files)
                    dc.build_images(
                        builds={image_tag: build}, current_version=__version__)
                else:
                    message += "\nRebuild it with:\n"
                    message += "$ rapydo --services %s" % build.get('service')
                    message += " build --rebuild-templates"
                    log.warning(message)

        if found_obsolete == 0:
            log.debug("No template build to be updated")

    def verify_obsolete_builds(
            self, docker_images, builds, overriding_imgs, template_builds):

        if len(builds) == 0:
            log.debug("No build to be verified")
            return

        found_obsolete = 0
        fmt = "%Y-%m-%d %H:%M:%S"
        for image_tag, build in builds.items():

            if image_tag not in docker_images:
                # Missing images will be created at startup
                continue

            build_is_obsolete = False
            message = ""

            # if FROM image is newer, this build should be re-built
            if image_tag in overriding_imgs:
                from_img = overriding_imgs.get(image_tag)
                from_build = template_builds.get(from_img)
                from_timestamp = self.get_build_timestamp(
                    from_build.get('timestamp'), as_date=True)
                build_timestamp = self.get_build_timestamp(
                    build.get('timestamp'), as_date=True)

                if from_timestamp > build_timestamp:
                    build_is_obsolete = True
                    b = build_timestamp.strftime(fmt)
                    c = from_timestamp.strftime(fmt)
                    message = "Image %s is obsolete" % image_tag
                    message += " (built on %s FROM %s" % (b, from_img)
                    message += " that changed on %s)" % c

            if not build_is_obsolete:
                # Check if some recent commit modified the Dockerfile
                obsolete, build_ts, last_commit = self.build_is_obsolete(build)
                if obsolete:
                    build_is_obsolete = True
                    b = datetime.fromtimestamp(build_ts).strftime(fmt)
                    c = last_commit.strftime(fmt)
                    message = "Image %s is obsolete" % image_tag
                    message += " (built on %s" % b
                    message += " but changed on %s)" % c

            if build_is_obsolete:
                found_obsolete += 1
                if self.current_args.get('rebuild'):
                    log.info("%s, rebuilding", message)
                    dc = Compose(files=self.files)

                    # Cannot force pull when building an image
                    # overriding a template build
                    force_pull = image_tag not in overriding_imgs
                    dc.build_images(
                        builds={image_tag: build},
                        force_pull=force_pull,
                        current_version=__version__
                    )
                else:
                    message += "\nRebuild it with:\n"
                    message += "$ rapydo --services %s" % build.get('service')
                    message += " build"
                    log.warning(message)

        if found_obsolete == 0:
            log.debug("No build to be updated")

    def bower_libs(self):

        if self.check or self.initialize or self.update:

            if self.frontend:
                bower_dir = os.path.join(
                    "data", self.project, "bower_components")

                install_bower = False
                if self.current_args.get('skip_bower'):
                    install_bower = False
                elif not os.path.isdir(bower_dir):
                    install_bower = True
                    os.makedirs(bower_dir)
                elif self.update:
                    install_bower = True
                else:
                    libs = helpers.list_path(bower_dir)
                    if len(libs) <= 0:
                        install_bower = True

                if install_bower:

                    if self.check:

                        # TODO: remove this check
                        # Added this check on 12th Sep 2017 just to help users
                        old_bdir = os.path.join("data", "bower_components")
                        if os.path.isdir(old_bdir):
                            log.exit(
                                """ The position of bower data dir changed!

Old position: %s
New position: %s

You can do several things:
- mkdir -p %s && mv %s %s
- execute rapydo init
- execute rapydo update
""" % (old_bdir, bower_dir, os.path.dirname(bower_dir), old_bdir, bower_dir)
                            )

                        #############################################

                        log.exit(
                            """Missing bower libs in %s
\nSuggestion: execute the init command"""
                            % bower_dir
                        )

                    else:

                        if self.initialize:
                            bower_command = "bower install"
                        else:
                            bower_command = "bower update"

                        bower_command += \
                            " --config.directory=/libs/bower_components"

                        dc = Compose(files=self.files)
                        dc.create_volatile_container(
                            "bower", command=bower_command)

                        log.info("Bower libs downloaded")

                elif self.current_args.get('skip_bower'):
                    log.info("Skipping bower checks")
                else:
                    log.checked("Bower libs already installed")

    def get_services(self, key='services', sep=',',
                     default=None
                     # , avoid_default=False
                     ):

        value = self.current_args.get(key).split(sep)
        # if avoid_default or default is not None:
        if default is not None:
            config_default = \
                self.arguments.parse_conf.get('options', {}) \
                .get('services') \
                .get('default')
            if value == [config_default]:
                # if avoid_default:
                #     log.exit("You must set '--services' option")
                if default is not None:
                    value = default
                else:
                    pass
        return value

    # def make_env(self, do=False):
    def make_env(self):
        envfile = os.path.join(helpers.current_dir(), COMPOSE_ENVIRONMENT_FILE)

        # if self.current_args.get('force_env'):
        if not self.current_args.get('cache_env'):
            try:
                os.unlink(envfile)
                log.verbose("Removed cache of %s" % COMPOSE_ENVIRONMENT_FILE)
            except FileNotFoundError:
                log.very_verbose("No %s to remove" % COMPOSE_ENVIRONMENT_FILE)

        if not os.path.isfile(envfile):

            with open(envfile, 'w+') as whandle:
                env = self.vars.get('env')
                env['PROJECT_DOMAIN'] = self.current_args.get('hostname')
                env['COMPOSE_PROJECT_NAME'] = self.current_args.get('project')
                # Relative paths from ./submodules/rapydo-confs/confs
                env['SUBMODULE_DIR'] = "../.."
                env['VANILLA_DIR'] = "../../.."

                env['RAPYDO_VERSION'] = __version__
                # FIXME: should be a parameter
                if self.current_args.get('privileged'):
                    env['DOCKER_PRIVILEGED_MODE'] = "true"
                else:
                    env['DOCKER_PRIVILEGED_MODE'] = "false"
                env.update({'PLACEHOLDER': PLACEHOLDER})

                for key, value in sorted(env.items()):
                    if value is None:
                        value = ''
                    else:
                        value = str(value)
                    # log.print("ENV values. %s:*%s*" % (key, value))
                    if ' ' in value:
                        value = "'%s'" % value
                    whandle.write("%s=%s\n" % (key, value))
                log.checked("Created %s file" % COMPOSE_ENVIRONMENT_FILE)

        else:
            log.very_verbose("Using cached %s" % COMPOSE_ENVIRONMENT_FILE)

    def check_placeholders(self):

        self.services_dict, self.active_services = \
            project.find_active(self.services)

        if len(self.active_services) == 0:
            log.exit(
                """You have no active service
\nSuggestion: to activate a top-level service edit your compose yaml
and add the variable "ACTIVATE: 1" in the service enviroment
                """)
        else:
            log.checked("Active services: %s", self.active_services)

        missing = []
        for service_name in self.active_services:
            service = self.services_dict.get(service_name)

            for key, value in service.get('environment', {}).items():
                if PLACEHOLDER in str(value):
                    missing.append(key)

        if len(missing) > 0:
            log.exit(
                "Missing critical params for configuration:\n%s" % missing)
        else:
            log.checked("No PLACEHOLDER variable to be replaced")

        return missing

    # def manage_one_service(self, service=None):

    #     if service is None:
    #         services = self.get_services(avoid_default=True)

    #         if len(services) != 1:
    #             log.exit(
    #                 "Commands can be executed only on one service." +
    #                 "\nCurrent request on: %s" % services)
    #         else:
    #             service = services.pop()

    #     return service

    def container_info(self, service_name):
        return self.services_dict.get(service_name, None)

    def container_service_exists(self, service_name):
        return self.container_info(service_name) is not None

    def get_ignore_submodules(self):
        ignore_submodule = self.current_args.get('ignore_submodule', '')
        if ignore_submodule is None:
            return ''
        return ignore_submodule.split(",")

    def git_checks(self):

        # TODO: give an option to skip things when you are not connected
        if not self.tested_connection:
            self.verify_connected()

        # FIXME: give the user an option to skip this
        # or eventually print it in a clearer way
        # (a table? there is python ascii table plugin)

        ignore_submodule_list = self.get_ignore_submodules()

        for name, gitobj in sorted(self.gits.items()):
            if name in ignore_submodule_list:
                log.debug("Skipping %s on %s" % (self.action, name))
                continue
            if gitobj is not None:
                if self.update:
                    gitter.update(name, gitobj)
                elif self.check:
                    gitter.check_updates(name, gitobj)
                    gitter.check_unstaged(name, gitobj)

    def custom_parse_args(self):

        # custom options from configuration file
        self.custom_commands = self.specs \
            .get('controller', {}).get('commands', {})

        if len(self.custom_commands) < 1:
            log.exit("No custom commands defined")

        for name, custom in self.custom_commands.items():
            self.arguments.extra_command_parser.add_parser(
                name, help=custom.get('description')
            )

        if len(self.arguments.remaining_args) != 1:
            self.arguments.extra_parser.print_help()
            import sys
            sys.exit(1)

        # parse it
        self.custom_command = \
            vars(
                self.arguments.extra_parser.parse_args(
                    self.arguments.remaining_args
                )
            ).get('custom')

    def rebuild_from_upgrade(self):
        log.warning("Rebuilding images from an upgrade")
        self.current_args['rebuild_templates'] = True
        self._build()

    ################################
    # ##    COMMANDS    ##         #
    ################################

    # TODO: make the commands availabe in this file in alphabetical order

    def _check(self):

        # NOTE: Do we consider what we have here a SECURITY BUG?
        # dc = Compose(files=self.files)
        # for container in dc.get_handle().project.containers():
        #     log.pp(container.client._auth_configs)
        #     exit(1)

        log.info("All checked")

    def _init(self):
        log.info("Project initialized")

    def _status(self):
        dc = Compose(files=self.files)
        dc.command('ps', {'-q': None})

    def _clean(self):
        dc = Compose(files=self.files)
        rm_volumes = self.current_args.get('rm_volumes', False)
        options = {
            '--volumes': rm_volumes,
            '--remove-orphans': True,
            '--rmi': 'local',  # 'all'
        }
        dc.command('down', options)

        log.info("Stack cleaned")

    def _update(self):
        log.info("All updated")

    def _start(self):
        if self.current_args.get('from_upgrade'):
            self.rebuild_from_upgrade()

        services = self.get_services(default=self.active_services)

        options = {
            'SERVICE': services,
            '--no-deps': False,
            '-d': True,
            # rebuild images changed with an upgrade
            '--build': self.current_args.get('from_upgrade'),
            # switching in an easier way between modules
            '--remove-orphans': True,  # False,
            '--abort-on-container-exit': False,
            '--no-recreate': False,
            '--force-recreate': False,
            '--no-build': False,
            '--scale': {},
        }

        dc = Compose(files=self.files)
        dc.command('up', options)

        log.info("Stack started")

    def _stop(self):
        services = self.get_services(default=self.active_services)

        options = {'SERVICE': services}

        dc = Compose(files=self.files)
        dc.command('stop', options)

        log.info("Stack stoped")

    def _restart(self):
        services = self.get_services(default=self.active_services)

        options = {'SERVICE': services}

        dc = Compose(files=self.files)
        dc.command('restart', options)

        log.info("Stack restarted")

    def _remove(self):
        services = self.get_services(default=self.active_services)

        dc = Compose(files=self.files)

        options = {
            'SERVICE': services,
            # '--stop': True,  # BUG? not working
            '--force': True,
            '-v': False,  # dangerous?
        }
        dc.command('stop')
        dc.command('rm', options)

        log.info("Stack removed")

    def _toggle_freeze(self):
        services = self.get_services(default=self.active_services)

        options = {'SERVICE': services}
        dc = Compose(files=self.files)
        command = 'pause'
        for container in dc.get_handle().project.containers():

            if container.dictionary.get('State').get('Status') == 'paused':
                command = 'unpause'
                break
        dc.command(command, options)

        if command == "pause":
            log.info("Stack paused")
        elif command == "unpause":
            log.info("Stack unpaused")

    def _log(self):
        dc = Compose(files=self.files)
        services = self.get_services(default=self.active_services)

        options = {
            '--follow': self.current_args.get('follow', False),
            '--tail': 'all',
            '--no-color': False,
            '--timestamps': True,
            'SERVICE': services,
        }

        try:
            dc.command('logs', options)
        except KeyboardInterrupt:
            log.info("Stopped by keyboard")

    def _interfaces(self):
        # db = self.manage_one_service()
        db = self.current_args.get('service')
        service = db + 'ui'

        # FIXME: this check should be moved inside create_volatile_container
        if not self.container_service_exists(service):
            log.exit("Container '%s' is not defined" % service)

        port = self.current_args.get('port')
        publish = []

        # FIXME: these checks should be moved inside create_volatile_container
        if port is not None:
            try:
                int(port)
            except TypeError:
                log.exit("Port must be a valid integer")

            info = self.container_info(service)
            try:
                current_ports = info.get('ports', []).pop(0)
            except IndexError:
                log.exit("No default port found?")

                # TODO: inspect the image to get the default exposed
                # $ docker inspect mongo-express:0.40.0 \
                #    | jq ".[0].ContainerConfig.ExposedPorts"
                # {
                #   "8081/tcp": {}
                # }

            publish.append("%s:%s" % (port, current_ports.target))

        dc = Compose(files=self.files)

        host = self.current_args.get('hostname')
        # FIXME: to be completed
        uris = {
            'swaggerui':
                # 'http://%s/swagger-ui/?url=http://%s:%s/api/specs' %
                # (host, host, '8080'),
                'http://%s?docExpansion=none' % host

        }

        uri = uris.get(service)
        if uri is not None:
            log.info(
                "You can access %s web page here:\n%s", service, uri)
        else:
            log.info("Launching interface: %s", service)
        with suppress_stdout():
            # NOTE: this is suppressing also image build...
            dc.create_volatile_container(service, publish=publish)

    def _shell(self, user=None, command=None, service=None):

        dc = Compose(files=self.files)
        service = self.current_args.get('service')
        # service = self.manage_one_service(service)

        if user is None:
            user = self.current_args.get('user')
            # if 'user' is empty, put None to get the docker-compose default
            if user is not None and user.strip() == '':
                if service in ['backend', 'restclient']:
                    user = 'developer'
                else:
                    user = None
        log.verbose("Command as user '%s'" % user)

        if command is None:
            default = 'echo hello world'
            command = self.current_args.get('command', default)

        return dc.exec_command(service, user=user, command=command)

    def _build(self):

        if self.current_args.get('rebuild_templates'):
            dc = Compose(files=self.base_files)
            log.debug("Forcing rebuild for cached templates")
            dc.build_images(self.template_builds, current_version=__version__)

        dc = Compose(files=self.files)
        services = self.get_services(default=self.active_services)

        options = {
            'SERVICE': services,
            # TODO: user should be allowed to set the two below from cli
            '--no-cache': False,
            '--pull': False,
        }
        dc.command('build', options)

        log.info("Images built")

    def _custom(self):
        log.debug("Custom command: %s" % self.custom_command)
        meta = self.custom_commands.get(self.custom_command)
        meta.pop('description', None)

        service = meta.get('service')
        user = meta.get('user', None)
        command = meta.get('command', None)
        dc = Compose(files=self.files)
        return dc.exec_command(service, user=user, command=command)

    def _ssl_certificate(self):

        current_method_name = "ssl-certificate"

        meta = self.arguments.parse_conf \
            .get('subcommands') \
            .get(current_method_name, {}) \
            .get('container_exec', {})

        # Verify all is good
        assert meta.pop('name') == 'letsencrypt'

        service = meta.get('service')
        user = meta.get('user', None)
        command = meta.get('command', None)
        dc = Compose(files=self.files)
        return dc.exec_command(service, user=user, command=command)
        # **meta ... explicit is not better than implicit???
        # return self._shell(**meta)

    def _ssl_dhparam(self):
        current_method_name = "ssl-dhparam"

        meta = self.arguments.parse_conf \
            .get('subcommands') \
            .get(current_method_name, {}) \
            .get('container_exec', {})

        # Verify all is good
        assert meta.pop('name') == 'dhparam'

        service = meta.get('service')
        user = meta.get('user', None)
        command = meta.get('command', None)
        dc = Compose(files=self.files)
        return dc.exec_command(service, user=user, command=command)

    def _bower_install(self):

        lib = self.current_args.get("lib", None)
        if lib is None:
            log.exit("Missing bower lib, please add the --lib option")

        current_method_name = "bower-install"

        meta = self.arguments.parse_conf \
            .get('subcommands') \
            .get(current_method_name, {}) \
            .get('container_exec', {})

        # Verify all is good
        assert meta.pop('name') == 'bower'

        conf_dir = "--config.directory=/libs/bower_components"
        bower_command = "bower install %s %s --save" % (conf_dir, lib)

        dc = Compose(files=self.files)
        dc.create_volatile_container("bower", command=bower_command)

    def _bower_update(self):

        lib = self.current_args.get("lib", None)
        if lib is None:
            log.exit("Missing bower lib, please add the --lib option")

        # Use my method name in a meta programming style
        # import inspect
        # current_method_name = inspect.currentframe().f_code.co_name
        current_method_name = "bower-install"

        meta = self.arguments.parse_conf \
            .get('subcommands') \
            .get(current_method_name, {}) \
            .get('container_exec', {})

        # Verify all is good
        assert meta.pop('name') == 'bower'

        conf_dir = "--config.directory=/libs/bower_components"
        bower_command = "bower update %s %s" % (conf_dir, lib)

        dc = Compose(files=self.files)
        dc.create_volatile_container("bower", command=bower_command)

    def _env(self):

        log.info("List of configured variables:")
        for var in sorted(self.current_args):
            val = self.current_args.get(var)
            print("%s: %s" % (var, val))

    def _template(self):
        service_name = self.current_args.get('service')
        force = self.current_args.get('yes')
        endpoint_name = self.current_args.get('endpoint')

        new_endpoint = EndpointScaffold(
            self.project, force, endpoint_name, service_name)
        new_endpoint.create()

    def _find(self):
        endpoint_name = self.current_args.get('endpoint')

        if endpoint_name is not None:
            lookup = EndpointScaffold(
                self.project, endpoint_name=endpoint_name)
            lookup.info()
        else:
            log.exit("Please, specify something to look for.\n" +
                     "Add --help to list available options.")

    def _scale(self):

        scaling = self.current_args.get('value', '')
        options = scaling.split('=')
        if len(options) != 2:
            log.exit("Please specify how to scale: SERVICE=NUM_REPLICA")
        else:
            service, workers = options

        services = self.get_services(default=self.active_services)
        # NOTE: scale has become an option of compose 'up'
        compose_options = {
            'SERVICE': services,
            '--no-deps': False,
            '-d': True,
            '--build': False,  # self.current_args.get('from_upgrade'),
            '--remove-orphans': True,
            '--abort-on-container-exit': False,
            '--no-recreate': False,
            '--force-recreate': False,
            '--no-build': False,
            # '--scale': {service: workers},
            '--scale': [scaling],
        }
        # print("TEST", service, workers)
        dc = Compose(files=self.files)
        dc.command('up', compose_options)

    def _coverall(self):

        basemsg = "COVERAGE cannot be computed"

        # Travis coverall.io token
        file = path.existing(['.', '.coveralls.yml'], basemsg)
        project.check_coveralls(file)
        # TODO: if missing link instructions on the website

        # Compose file with service > coverage
        from utilities import CONF_PATH
        compose_file = path.existing(['.', CONF_PATH, 'coverage.yml'], basemsg)
        service = project.check_coverage_service(compose_file)
        # TODO: if missing link a template

        # Copy coverage file from docker
        self.vars.get('env')
        covfile = '.coverage'
        mittdir = '/code'
        destdir = '.'
        self.docker.copy_file(
            service_name='backend',
            containers_prefix=self.project,
            mitt=str(path.join(mittdir, covfile)),
            dest=str(path.join(destdir, covfile)),
        )

        # Coverage file where coverage percentage was saved
        path.existing(['.', covfile], basemsg)
        # NOTE: should not be missing if the file above is from the template

        # Execute
        options = {
            'SERVICE': [service],
            '--no-deps': False,
            '-d': False,
            '--abort-on-container-exit': True,
            '--remove-orphans': False,
            '--no-recreate': True,
            '--force-recreate': False,
            '--build': False,
            '--no-build': False,
            '--no-color': False,
            '--scale': ['%s=1' % service]
        }
        dc = Compose(files=[compose_file])

        # FIXME: check if this command could be 'run' instead of using 'up'
        dc.command('up', options)

    def available_releases(self, releases, current_release):

        log.warning('List of available releases:')
        print('')
        for release, info in releases.items():

            r = info.get("rapydo")
            t = info.get('type')

            if release == current_release:
                extra = " *installed*"
            else:
                extra = ""

            print(' - %s %s (rapydo %s) [%s]%s' %
                  (release, t, r, info.get('status'), extra))
        print('')

    def preliminary_upgrade_checks(self, current_release, new_release):
        if current_release == 'master':
            log.exit("Cannot upgrade from master. Please work on a branch.")

        if new_release is None:
            self.available_releases(self.releases, current_release)
            return False

        if new_release == ".":
            if current_release not in self.releases:
                self.available_releases(self.releases, current_release)
                log.exit('Release %s not found' % current_release)

            return True

        if new_release not in self.releases:
            self.available_releases(self.releases, current_release)
            log.exit('Release %s not found' % new_release)

        if new_release == current_release:
            log.error('You are already using release %s' % current_release)
            return False

        log.info('Requested release: %s' % new_release)

        if not self.current_args.get('downgrade'):
            try:
                if LooseVersion(new_release) < LooseVersion(current_release):
                    log.exit('Cannot upgrade to previous version')
            except TypeError as e:
                log.exit("Unable to compare %s with %s (%s)" % (
                    new_release, current_release, e)
                )

        status = self.releases.get(new_release).get('status')
        if status == STATUS_DISCONTINUED:
            log.exit("This version is discontinued")
        elif status == STATUS_RELEASED:
            pass
        elif status == STATUS_DEVELOPING:
            if self.development:
                log.verbose("Switching to a developing version")
            else:
                log.exit("This version has yet to be released")
        else:
            log.exit("%s: unknown version status: %s", new_release, status)

        return True

    def _upgrade(self):
        if len(self.releases) < 1:
            log.exit('This project does not support releases yet')

        gitobj = self.gits.get('main')
        current_release = gitter.get_active_branch(gitobj)
        if self.current_args.get('current'):
            new_release = "."
        else:
            new_release = self.current_args.get('release')
        log.info('Current release: %s' % current_release)

        # To reduce the function complexity, I moved all preliminary check in
        # a dedicated function. Note: that function can stop with log.exit
        if not self.preliminary_upgrade_checks(current_release, new_release):
            return False

        # # 0. if current main repo is being developed, stop this
        # # NOTE: I am not checking for commits to be pushed
        main_repo = self.gits.pop('main')
        if gitter.check_unstaged('main', main_repo):
            log.exit('Interrupting')

        # 1. check submodules versions
        # if different move current to `submodules/.backup/$VERSION/$TOOL`
        for name, gitobj in sorted(self.gits.items()):

            # Skip non existing submodules or missing
            if gitobj is None:
                continue

            if gitter.check_unstaged(name, gitobj):
                current_dir = gitobj.working_dir
                msg = "Unable to upgrade"
                msg += "\n\nYou have unstaged files in: %s" % current_dir
                msg += "\n\nPlease commit or undo these changes,"
                msg += " then retry the upgrade\n"
                log.exit(msg)
                # current_version = gitter.get_active_branch(gitobj)
                # backup_dir = helpers.current_fullpath(
                #     SUBMODULES_DIR, '.backup', current_version, name)
                # import shutil
                # try:
                #     shutil.move(current_dir, backup_dir)
                # except BaseException as e:
                #     log.exit(
                #         name, e.__class__.__name__, e)
                # log.info("Safety backup:\n%s -> %s", current_dir, backup_dir)

        # 2. git checkout new version
        if new_release == ".":
            log.debug("Switch branch not required")
        elif gitter.switch_branch(main_repo, new_release):  # , remote=False):
            log.info("Main active branch: %s", new_release)
        else:
            log.exit("Failed switching main repository to %s", new_release)

        # 3. reinit submodules
        self.read_specs()  # read again project configuration!
        if not self.verify_rapydo_version(do_exit=False):
            log.info("Trying to install controller %s", self.rapydo_version)
            from utilities.packing import install, check_version

            package = "rapydo-controller"

            if install("%s==%s" % (package, self.rapydo_version)):
                installed_version = check_version(package)
                installed = (installed_version != self.rapydo_version)
            else:
                installed = False

            if not installed:
                log.error(
                    "Failed to install %s %s", package, self.rapydo_version)
                log.warning(
                    "Rolling back previous branch on main repository")
                if gitter.switch_branch(main_repo, current_release):
                    log.info("Main repository back to %s", current_release)
                else:
                    log.error(
                        "Failed switching main repository to %s",
                        current_release)
                log.exit("Upgrade failed")

        self.initialize = True
        self.git_submodules()

        # 4. rebuild images
        self.rebuild_from_upgrade()

        # 5. safely restart?
        # docker-compose up --force-recreate

    ################################
    # ### RUN ONE COMMAND OFF
    ################################

    def run(self):
        """
        RUN THE APPLICATION!
        The heart of the app: it runs a single controller command.
        """

        # Initial inspection
        self.get_args()
        self.check_installed_software()
        self.inspect_main_folder()
        self.git_submodules(confs_only=True)
        self.check_projects()
        self.read_specs()  # read project configuration
        self.verify_rapydo_version()
        self.inspect_project_folder()

        # Generate and get the extra arguments in case of a custom command
        if self.action == 'custom':
            self.custom_parse_args()
        else:
            try:
                argname = next(iter(self.arguments.remaining_args))
            except StopIteration:
                pass
            else:
                log.exit(
                    "Unknown argument:'%s'.\nUse --help to list options",
                    argname)

        # Verify if we implemented the requested command
        function = "_%s" % self.action.replace("-", "_")
        func = getattr(self, function, None)
        if func is None:
            log.exit(
                "Command not yet implemented: %s (expected function: %s)"
                % (self.action, function))

        # Detect if heavy ops are allowed
        do_heavy_ops = False
        do_heavy_ops = self.update or self.check
        if self.check:
            if self.current_args.get('skip_heavy_git_ops', False):
                do_heavy_ops = False

        self.git_submodules(confs_only=False)

        # GIT related
        if do_heavy_ops:
            self.git_checks()  # NOTE: this might be an heavy operation
        else:
            log.verbose("Skipping heavy operations")

        # if self.check:

        #     remote_branch = self.vars.get(
        #         'repos', []).get(
        #         'core', []).get(
        #         'branch', 'master')

        #     if self.current_args.get('verify_upstream', False):
        #         # FIXME: connection verification should be made only once
        #         self.verify_connected()
        #         gitter.check_updates(
        #             'upstream', self.gits['main'],
        #             fetch_remote='upstream',
        #             remote_branch=remote_branch
        #         )

        # self.make_env(do=do_heavy_ops)
        self.make_env()

        # Compose services and variables
        self.read_composers()
        self.check_placeholders()

        # Build or check template containers images
        self.build_dependencies()

        # Install or check bower libraries (if frontend is enabled)
        self.bower_libs()

        # Final step, launch the command
        func()

    # issues/57
    # I'm temporary here... to be decided how to handle me
    def get_reserved_project_names(self):
        names = [
            'abc',
            'attr',
            'base64',
            'better_exceptions',
            'bravado_core',
            'celery',
            'click',
            'collections',
            'datetime',
            'dateutil',
            'elasticsearch_dsl',
            'email',
            'errno',
            'flask',
            'flask_injector',
            'flask_oauthlib',
            'flask_restful',
            'flask_sqlalchemy',
            'functools',
            'glob',
            'hashlib',
            'hmac',
            'injector',
            'inspect',
            'io',
            'irods',
            'iRODSPickleSession',
            'json',
            'jwt',
            'logging',
            'neo4j',
            'neomodel',
            'os',
            'pickle',
            'plumbum',
            'pymodm',
            'pymongo',
            'pyotp',
            'pyqrcode',
            'pytz',
            'random',
            're',
            'smtplib',
            'socket',
            'sqlalchemy',
            'string',
            'submodules',
            'sys',
            'time',
            'unittest',
            'werkzeug'
        ]
        return names
