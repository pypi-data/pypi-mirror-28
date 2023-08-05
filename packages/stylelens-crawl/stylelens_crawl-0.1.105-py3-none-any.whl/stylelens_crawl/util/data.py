import os
import re
import json
from stylelens_crawl import BASE_DIR, PKG_DIR
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

RANGE_RE = re.compile(r'^[$]?([A-Z]+)[$]?(\d+)$')


def get_value_from_url(url, var):
    find_no = url[url.find(var):]
    if find_no.find('&') > 0:
        find_no = find_no[:find_no.find('&')]
    find_no = find_no.split('=')[-1]
    return find_no


def get_cate_no(platform, **kwargs):
    url = kwargs.get('url', False)
    prd_var = kwargs.get('var', False)

    if not url:
        raise RuntimeError('The url value not exist.')

    if platform == 'CAFE24':

        if prd_var:
            if url.find(prd_var) > -1:
                return int(get_value_from_url(url, prd_var))

        seperated_url = url.split(sep='/')

        if len(seperated_url) >= 5:
            return int(seperated_url[-6])

        return ''


def get_product_no(platform, **kwargs):
    url = kwargs.get('url', False)
    prd_var = kwargs.get('product_var', False)

    if not url:
        raise RuntimeError('The url value not exist.')

    if platform == 'CAFE24':

        if prd_var:
            if url.find(prd_var) > -1:
                return get_value_from_url(url, prd_var)

        seperated_url = url.split(sep='/')

        if len(seperated_url) >= 5:
            return seperated_url[-6]

        return ''


class CsvToDict(object):
    def __init__(self, headers, ranges=None):
        self.headers = headers
        self.ranges = ranges

    def make_a_header_with_ranges(self):
        assert self.headers, 'The headers value is None'
        assert self.ranges, 'The ranges values is None'

        mat = RANGE_RE.match(self.ranges.split(sep='!')[-1].split(sep=':')[0])

        assert mat, 'The range format is wrong'

        column, _ = mat.groups()

        converted_header = {}
        for header in self.headers:
            converted_header[header] = column
            column = chr(ord(column) + 1)

        return converted_header

    def convert_csv_to_dict(self, rows):
        output = []
        for row in rows:
            converted_row = {}
            for idx, header in enumerate(self.headers):
                if idx == len(row):
                    break
                converted_row[header] = row[idx]

            output.append(converted_row)

        return output


class SpreadSheets(object):
    def __init__(self, sheet_id, scope=None, key_path=None):
        if sheet_id is None:
            raise RuntimeError('The sheetid value is None.')

        if not scope:
            scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']

        if not key_path:
            if os.path.exists('/tmp/gdoc_certi.json'):
                key_path = '/tmp/gdoc_certi.json'
            elif os.path.exists(os.path.join(PKG_DIR, 'cred/f3c4bf11ae96.json')):
                key_path = os.path.join(PKG_DIR, 'cred/f3c4bf11ae96.json')
            else:
                raise RuntimeError('The key file is not exist.')

        credentials = ServiceAccountCredentials.from_json_keyfile_name(key_path, scope)
        self.service = discovery.build('sheets', 'v4', credentials=credentials)
        self.sheet_id = sheet_id

    def get_rows(self, ranges):
        return self.service.spreadsheets().values().get(spreadsheetId=self.sheet_id, range=ranges).execute().get(
            'values', [])

    def get_rows_with_header(self, ranges):
        result = self.service.spreadsheets().values().get(spreadsheetId=self.sheet_id, range=ranges).execute().get(
            'values', [])
        return CsvToDict(headers=result.pop(0)).convert_csv_to_dict(result)

    def update_item_with_column_key(self, ranges, item, value_input_option='USER_ENTERED'):
        return self.service.spreadsheets().values().get(spreadsheetId=self.sheet_id, range=ranges,
                                                        valueInputOption=value_input_option, body={
                                                            'values': item
                                                        }).execute()


class Menu(object):
    def __init__(self, raw_json, visible_cate_url_list, option=None):
        visible_cate_list = []
        parsed_json = json.loads(raw_json, encoding='UTF-8')
        self.dict_data = {
            'name': [],
            'cate_no': [],
            'parent_cate_no': [],
            'link_product_list': [],
        }

        for item in parsed_json:
            self.dict_data['name'].append(item['name'])
            self.dict_data['cate_no'].append(item['cate_no'])
            self.dict_data['parent_cate_no'].append(item['parent_cate_no'])
            self.dict_data['link_product_list'].append(item['link_product_list'])
            if not option:
                if item['link_product_list'] in visible_cate_url_list:
                    visible_cate_list.append(item['cate_no'])

        if option:
            if option == 1:
                for cate_url in visible_cate_url_list:
                    visible_cate_list.append(get_cate_no('CAFE24', url=cate_url, var='cate_no'))
            elif option == 2:
                visible_cate_list.append(1)

        self.visible_cate_list = visible_cate_list
        self.target_cate_list = visible_cate_list
        self.search_data = []

    def __get_child_cate_list(self, cate_no):
        for idx, val in enumerate(self.dict_data['parent_cate_no']):
            if val == cate_no:
                self.target_cate_list.append(self.dict_data['cate_no'][idx])
                if self.dict_data['cate_no'][idx] in self.dict_data['parent_cate_no']:
                    self.__get_child_cate_list(self.dict_data['cate_no'][idx])

    def __get_visible_cate(self):
        for cate_no in self.visible_cate_list:
            self.__get_child_cate_list(cate_no=cate_no)

    def get_cate_list(self):
        self.__get_visible_cate()
        for idx, cate_no in enumerate(self.dict_data['cate_no']):
            if cate_no not in self.dict_data['parent_cate_no'] and self.dict_data['parent_cate_no'][idx] in \
                    self.dict_data['cate_no'] and cate_no in self.target_cate_list:
                self.search_data.append(self.dict_data['link_product_list'][idx])

        return self.search_data
