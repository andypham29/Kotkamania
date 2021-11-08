import time

import requests

from setting import Setting


class FantasyHotStreakScript:

    def __init__(self):
        pass

    def run(self):
        for i in range(10):
            start_time = time.time()
            response = self.run_script(i)
            body = response.content.decode('utf-8')
            code = response.status_code
            print(f"[{code}] {body} {round(time.time() - start_time, 3)}s")
        print("done")

    def run_script(self, offset):
        # url = f'https://nhlmockdraft2020.herokuapp.com/admin/script/{offset}'
        url = f'http://localhost:5000/admin/script/{offset}'
        api_key = Setting.KKMANIA_API_KEY
        headers = {'x-api-key': f'{api_key}'}

        return requests.get(url=url, headers=headers)


if __name__ == "__main__":
    FantasyHotStreakScript().run()
