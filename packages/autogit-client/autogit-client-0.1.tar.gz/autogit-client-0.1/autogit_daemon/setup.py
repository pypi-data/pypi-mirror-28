import json
import os
import sys
import argparse
import time

import requests

from daemon import Daemon
from utils import *

total_argv = len(sys.argv)
cmdargs = str(sys.argv)

BETA_URL = "https://beta-dashboard.autogit.io"
PRODUCTION_URL = "https://dashboard.autogit.io"
CHECKER_URL = "http://checker.autogit.io"


class AutoGitSetup(Daemon):
    def __init__(self, secret=None, access=None, server=None):
        Daemon.__init__(self, pidfile='/tmp/autogit-daemon.pid')
        self.autogit_server = self.set_server(server)
        self.current_data = {}
        self.env = os.environ.copy()
        self.secret = secret
        self.access = access
        self.info = {}
        self.server_id = ''
        self.temp_list = []
        self.DEFAULT_PATH = '/var/www/'
        self.TEMP_LOCATION = os.environ.get('HOME') + "/TEMP"

    def set_server(self, server):
        request = requests.get(CHECKER_URL).text

        if server:
            return server
        elif "True" in request:
            return BETA_URL
        else:
            return PRODUCTION_URL

    def validate_keys(self):

        if self.access and self.secret:
            validated = requests.post("%s/validate/" % self.autogit_server,
                                      data=dict(secret_key=self.secret, access_key=self.access))
            validated = validated.json()

            if validated['status'] == 'SUCCESS':
                self.DEFAULT_PATH = validated['result']['path']
                self.server_id = validated['result']['server_id']

                if self.check_env_variable():
                    self.update_env_variables()
                else:
                    self.create_env_variables()
                return True

        elif self.check_env_variable():
            validated = requests.post("%s/validate/" % self.autogit_server,
                                      data=dict(secret_key=self.env.get('AUTOGIT_SECRET_KEY', None),
                                                access_key=self.env.get('AUTOGIT_ACCESS_KEY', None)))
            validated = validated.json()
            if validated['status'] == 'SUCCESS':
                self.DEFAULT_PATH = validated['result']['path']
                self.server_id = validated['result']['server_id']

                self.update_env_variables()
                return True
        return False

    def create_env_variables(self):
        if not os.path.isfile("~/.autogit"):
            open("~/.autogit", 'x')
        os.system("echo '\nexport AUTOGIT_SECRET_KEY=%s' >> ~/.autogit" % (self.secret))
        os.system("echo 'export AUTOGIT_ACCESS_KEY=%s' >> ~/.autogit" % (self.access))
        os.system(". ~/.autogit")

    def check_env_variable(self):
        return bool(self.env.get('AUTOGIT_SECRET_KEY', False)) and bool(
            self.env.get('AUTOGIT_ACCESS_KEY', False))

    def update_env_variables(self):
        # delete the last 2 lines of a file
        for x in range(0, 2):
            os.system('sed -i "$ d" {0}'.format('~/.autogit'))
        self.create_env_variables()

    def fetch_params(self):
        info = requests.post(
            "%s/deploy/" % (self.autogit_server),
            data=dict(server_id=self.server_id,
                      secret_key=self.secret,
                      access_key=self.access))
        if self.is_fetch_success(info):
            self.info = info.json()

    def is_fetch_success(self, info):
        return info.json()['status'] == 'SUCCESS'

    def checkPath(self):
        try:
            return os.path.isdir(self.DEFAULT_PATH + self.info['repo']) and \
                   os.path.basename(self.DEFAULT_PATH + self.info['repo']) == self.info['repo']
        except:
            return False

    def execute_commands(self):
        try:
            status = "SUCCESS"
            self.backup_repo()
            os.chdir(self.DEFAULT_PATH + self.info['repo'])

            self.remove_all_branch_except_the_current()

            fetch = os.popen("git fetch -ap %s" % self.git_auth()).read()
            os.system("git config --global credential.helper 'cache'")
            reset = os.popen("git reset --hard").read()
            stash = os.popen("git stash").read()
            clean = os.popen("git clean -xdf").read()
            checkout = os.popen("git checkout %s" % self.info['branch']).read()
            pull = os.popen("git pull origin %s" % self.info['branch']).read()

            exec_yml = self.yml_file()
            status = exec_yml['status']

            self.rsync_repo()

            return {'fetch': fetch, 'reset': reset, 'stash': stash, 'clean': clean,
                    'checkout': checkout, 'branch_name': self.info['branch'], 'repo': self.info['repo'], 'pull': pull,
                    'yml': exec_yml['logs'], 'status': status}
        except:
            return {'status': 'FAILED'}

    def yml_file(self):
        errors_message = ["error", "traceback", "unknown command"]
        try:
            os.chdir(self.DEFAULT_PATH + self.info['repo'])
            ls = os.popen("ls").read().split("\n")

            if not "autogit.yml" in ls:
                """no yml file"""
                return {"status": "SUCCESS", "logs": []}

            lists = open("autogit.yml", 'r').read().split("\n")
            logs = []

            for line in lists:
                if line and line[0] != "#":
                    run = os.popen(line).read()
                    for error in errors_message:
                        if error in run.lower():
                            print(run)
                            logs.append({"command": line, "message": run})
                            return {"status": "FAILED", "logs": logs}
                    logs.append({"command": line, "message": run})

            return {"status": "SUCCESS", "logs": logs}

        except:
            return {"status": "SUCCESS", "logs": []}

    def remove_all_branch_except_the_current(self):
        try:
            branch_list = os.popen("git branch").read()
            lists = get_list_of_branch(branch_list)
            [os.system('git branch %s -d' % branch) for branch in lists]
        except:
            pass

    def git_auth(self):
        if self.info['repo_owner']:
            return 'https://' + self.info['username'] + ':' + self.info['token'] + '@' \
                   + self.info['url'] + '/' + self.info['repo_owner'] + '/' + self.info['repo']
        return 'https://' + self.info['username'] + ':' + self.info['token'] + '@' \
               + self.info['url'] + '/' + self.info['username'] + '/' + self.info['repo']

    def backup_repo(self):
        os.chdir(self.DEFAULT_PATH + self.info['repo'])
        ignore_list = self.gitignore_list()
        self.create_or_view_temporary_location()
        self.temp_list = []

        for name in ignore_list:
            try:
                if name[-1] == "/":
                    name = name.replace(name[-1], '')
                self.temp_list.append(name)
                os.system("rsync -aLdrz %s%s/%s %s" % (self.DEFAULT_PATH, self.info['repo'], name, self.TEMP_LOCATION))
            except:
                pass

    def create_or_view_temporary_location(self):
        if not os.path.exists(self.TEMP_LOCATION):
            os.makedirs(self.TEMP_LOCATION)

    def gitignore_list(self):
        return open(".gitignore", 'r').read().split("\n")

    def rsync_repo(self):
        os.chdir(self.TEMP_LOCATION)
        list = self.get_temp_list()
        for temp in self.temp_list:
            for name in list:
                if name in temp:
                    temp = temp.replace(name, '')
                    os.system(
                        "rsync -azv --remove-source-files %s/%s %s/%s/%s" % (
                            self.TEMP_LOCATION, name, self.DEFAULT_PATH, self.info['repo'], temp))
                    break

    def get_temp_list(self):
        return os.popen("ls").read().split("\n")[:-1]

    def _setup(self):
        try:
            self.fetch_params()
        except:
            pass

        if self.checkPath() and self.current_data != self.info:
            logs = self.execute_commands()

            time.sleep(5)

            post = requests.post("%s/worker/log/" % self.autogit_server,
                                 data=dict(logs=json.dumps(logs), repository=self.info['repo'],
                                           branch_id=self.info['branch_id'], server_id=self.server_id))
            post = post.json()
            if post['status'] == 'SUCCESS':
                self.current_data = self.info

    def run(self):
        if self.validate_keys():
            while True:
                time.sleep(1)
                self._setup()
        else:
            Daemon.stop(self)
            sys.exit("Invalid keys")


def main():
    git = AutoGitSetup()
    if total_argv == 2:
        if 'start' == sys.argv[1]:
            git.start()
            # git.run()  # for testing to see logs
        elif 'stop' == sys.argv[1]:
            git.stop()
        elif 'restart' == sys.argv[1]:
            git.restart()
        else:
            print("Unknown command")
            sys.exit(2)

    elif total_argv > 2:

        parser = argparse.ArgumentParser(description='AutoGit Daemon Setup')
        parser.add_argument('--secret', type=str, help='Secret key')
        parser.add_argument('--access', type=str, help='Access key')
        parser.add_argument('--server', type=str, help='Server URL')

        args = parser.parse_args()
        git.__init__(secret=args.secret, access=args.access, server=args.server)
        git.start()  # start as daemon
        # git.run()  # for testing to see logs

    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
