# Python standard library modules
import datetime
import os
import subprocess
import threading
import time


class HealthCheckRunner(threading.Thread):
    def __init__(self, config, results):
        self.config = config
        self.results = results
        threading.Thread.__init__(self)

    def run(self):
        while True:
            new_status = True
            new_check_data = {'pass': [], 'fail': []}

            for script in os.listdir(self.config['scripts_path']):
                try:
                    child = subprocess.Popen(
                        [os.path.join(self.config['scripts_path'], script)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                    )
                except:
                    new_status = False
                    new_check_data['fail'].append({
                        'script': os.path.join(self.config['scripts_path'], script),
                        'return_code': None,
                        'output': '<Script failed to execute>',
                    })
                    continue

                stdout, stderr = child.communicate()
                return_code = child.returncode

                if return_code != 0:
                    new_status = False

                    new_check_data['fail'].append({
                        'script': os.path.join(self.config['scripts_path'], script),
                        'return_code': return_code,
                        'output': stdout,
                    })
                else:
                    new_check_data['pass'].append({
                        'script': os.path.join(self.config['scripts_path'], script),
                        'return_code': return_code,
                        'output': stdout,
                    })

            self.results['all_ok'] = new_status
            self.results['check_data'] = new_check_data
            self.results['last_check'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Wait before starting the next round of checks
            time.sleep(self.config['sleep_time'])
