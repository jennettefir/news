import base64
import json
import os
import subprocess
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Tuple, Dict, List

import requests
from requests import Response

from articles_scrapers.utils.constants import STATUS_SUCCESS, STATUS_FAILED
from articles_scrapers.utils.types import RewriteType
from database.queries.queries import select_unprocessed_rewrites, insert_in_progress_rewrite, update_in_progress_rewrite
from translate_transition import ReWriter
from . import BaseCommand


class GenerateRewriteCommand(BaseCommand):
    endpoints = []

    def __init__(self):
        super(GenerateRewriteCommand, self).__init__()

    def init(self):
        pass

    def add_options(self, parser):
        super().add_options(parser)

        parser.add_option("--rewrite_type",
                          type="str",
                          help='''rewrite type: ["translate", "quillbot", "gpt2"]''')
        parser.add_option("--num_workers", type=int, help='''number of threads for articles processing''', default=8)

        (options, args) = parser.parse_args()
        if not options.rewrite_type:
            parser.error('rewrite_type not given')

        try:
            options.rewrite_type = RewriteType(options.rewrite_type)
        except ValueError as e:
            parser.error(str(e))

    def run(self, args, opts):
        rewrite_type: RewriteType = RewriteType(opts.rewrite_type)
        wrapper_function = self.get_wrapper_by_type(rewrite_type)
        self.validate_rewrite_type_run(rewrite_type)
        rewrites: Tuple[Dict] = self.select_unprocessed_rewrite(rewrite_type)
        self.load_endpoints()
        self.logger.info(f"WORKERS NUM = {opts.num_workers}")

        with ThreadPoolExecutor(max_workers=opts.num_workers) as pool:
            for idx, (processed_text, rewrite_record) in enumerate(pool.map(wrapper_function, rewrites)):
                try:
                    self.send_to_wordpress_api(processed_text, rewrite_record, rewrite_type)
                    update_in_progress_rewrite({
                        'article_id': rewrite_record['id'],
                        'error': None,
                        'status': STATUS_SUCCESS,
                        'rewrite_type': rewrite_type.name
                    })
                except Exception as e:
                    error: str = repr(e)
                    self.logger.warning(error)
                    update_in_progress_rewrite({
                        'article_id': rewrite_record['id'],
                        'error': error,
                        'status': STATUS_FAILED,
                        'rewrite_type': rewrite_type.name
                    })

    def translate_wrapper(self, rewrite_record: Dict) -> Tuple[str, Dict]:
        source_text = self.get_source_text(rewrite_record)
        return ReWriter(source_text).run(), rewrite_record

    def quillbot_wrapper(self, rewrite_record: Dict) -> Tuple[str, Dict]:
        path_to_source_file = self.get_path_to_file(rewrite_record)
        path_to_dir, file = path_to_source_file.rsplit(os.sep, 1)

        subprocess.call(['python', 'quillbot_launcher.py', path_to_source_file])

        path_to_result_file = os.path.join(path_to_dir, file.replace('.txt', '_quill_rewrite.txt'))
        with open(path_to_result_file, 'rt', encoding='utf8') as reader:
            return reader.read(), rewrite_record

    def gpt2_wrapper(self, rewrite_record: Dict) -> Tuple[str, Dict]:
        source_text = self.get_source_text(rewrite_record)
        result = requests.post(
            self.settings.get("GPT2_MODEL_API").rstrip("/") + "/text_rewrite",
            json={"text": source_text},
            timeout=4000
        ).json()['output']
        return result, rewrite_record

    def send_to_wordpress_api(self, processed_text: str, rewrite_record: Dict, rewrite_type: RewriteType):
        for api_endpoint in self.get_wordpress_blog_api_endpoints(rewrite_type):
            data_string = ':'.join([api_endpoint['user'], api_endpoint['password']])
            token = base64.b64encode(data_string.encode())
            headers = {'Authorization': 'Basic ' + token.decode('utf-8')}

            post = {
                'date': rewrite_record['publication_date'].isoformat() if rewrite_record['publication_date'] else None,
                'title': rewrite_record['title'],
                'status': 'publish',
                'content': processed_text,
                'author': 1,
                'format': 'standard',
                'tags': [],
            }

            response: Response = requests.post(
                api_endpoint['url'],
                headers=headers,
                json=post)

            self.logger.info(f'Crawled {response.status_code} <POST {response.request.method} {response.url}>')

            if not (200 <= response.status_code < 300):
                raise Exception(response.text)
        return True

    def get_path_to_file(self, rewrite_record: Dict) -> str:
        return os.path.join(os.getcwd(), 'files', rewrite_record['text_filepath'])

    def get_source_text(self, rewrite_record: Dict):
        path_to_file = self.get_path_to_file(rewrite_record)
        with open(path_to_file, 'rt', encoding='utf8') as reader:
            return reader.read()

    def validate_rewrite_type_run(self, rewrite_type: RewriteType):
        if rewrite_type.name == "gpt2":
            try:
                requests.get(self.settings.get("GPT2_MODEL_API"), timeout=5)
            except Exception as e:
                self.logger.error("GPT-2 SERVER IS NOT AVAILABLE NOW")
                self.logger.error(str(repr(e)))
                raise Exception("GPT-2 SERVER IS NOT AVAILABLE NOW")

    def get_wrapper_by_type(self, rewrite_type: RewriteType):
        if rewrite_type.name == 'translate':
            return self.translate_wrapper
        elif rewrite_type.name == 'gpt2':
            return self.gpt2_wrapper
        elif rewrite_type.name == 'quillbot':
            return self.quillbot_wrapper
        raise Exception('unsupported rewrite type')

    def get_wordpress_blog_api_endpoints(self, rewrite_type: RewriteType):
        for endpoint in self.endpoints:
            if endpoint['rewrite_type'] == rewrite_type.name:
                yield {
                    "url": f'{endpoint["url"]}?rest_route=/wp/v2/posts',
                    "user": endpoint["user"],
                    "password": endpoint["password"]
                }

    def select_unprocessed_rewrite(self, rewrite_type: RewriteType):
        records: Tuple[Dict] = select_unprocessed_rewrites(rewrite_type)
        article_ids: Tuple[int] = tuple(int(i['id']) for i in records)
        insert_in_progress_rewrite(rewrite_type, article_ids)
        return records

    def load_endpoints(self):
        with open("endpoints.config.json", encoding='utf-8') as f:
            self.endpoints = json.load(f)
