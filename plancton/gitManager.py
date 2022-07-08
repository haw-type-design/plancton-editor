import subprocess

class gitManager:
    def __init__(self):
        self.project_path = ''
        pass

    def branch_list(self):
        result = subprocess.Popen(
                ['git', '-C', self.project_path, 'branch', '-q'],
                stdout=subprocess.PIPE
                )
        re = result.communicate()[0].decode('UTF-8')
        print(result.returncode)
        print(dir(result))
        return re.replace(' ', '').split('\n')

    def checkout_branch(self, branch):
        result = subprocess.Popen(
                ['git', '-C', self.project_path, 'checkout', branch],
                stdout=subprocess.PIPE
                )
        re = result.communicate()[0].decode('UTF-8')
        return str(result)

    def new_branch(self, branch):
        result = subprocess.Popen(
                ['git', '-C', self.project_path, 'checkout', '-b', branch],
                stdout=subprocess.PIPE
                )
        re = result.communicate()[0].decode('UTF-8')
        return str(result)

    def delete_branch(self, branch):
        result = subprocess.Popen(
                ['git', '-C', self.project_path, 'branch', '-d', branch],
                stdout=subprocess.PIPE
                )
        re = result.communicate()[0].decode('UTF-8')
        return str(result)
    
    def add(self, files):
        result = subprocess.Popen(
                ['git', '-C', self.project_path, 'add', files],
                stdout=subprocess.PIPE
                )
        re = result.communicate()[0].decode('UTF-8')
        return str(result)

    def commit(self, message):
        result = subprocess.Popen(
                ['git', '-C', self.project_path, 'commit', '-m', message],
                stdout=subprocess.PIPE
                )
        re = result.communicate()[0].decode('UTF-8')
        return str(result)
    
    def pull(self, branch):
        result = subprocess.Popen(
                ['git', '-C', self.project_path, 'pull', 'origin', branch],
                stdout=subprocess.PIPE
                )
        re = result.communicate()[0].decode('UTF-8')
        return str(result)
   
    def push(self, branch):
        result = subprocess.Popen(
                ['git', '-C', self.project_path, 'push', 'origin', branch],
                stdout=subprocess.PIPE
                )
        re = result.communicate()[0].decode('UTF-8')
        return str(result)

    def save(self, files, branch, message):
        result = self.add(files)
        result = self.commit(message)
        result = self.pull(branch)
        result = self.push(branch)

