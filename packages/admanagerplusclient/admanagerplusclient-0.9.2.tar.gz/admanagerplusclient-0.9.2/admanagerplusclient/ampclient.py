#!/usr/bin/env python

from future.standard_library import install_aliases
install_aliases()


import json
import jwt
import requests
import time
import os
import base64

import sys
# if sys.version_info < (3, 0):
#     raise "must use python 2.5 or greater"

use_environment_variables = None

try:
    from django.conf import settings
except ImportError:
    use_environment_variables = True

class SiteList:
    id = None
    name = None
    accountId = 0
    status = None
    list_type = None
    isShared = None
    childrenCount = None
    updatedAt = None
    items = []
    br_client = None
    
    def __init__(self, br_client):
        self.br_client = br_client

    def read_by_id(self, cid):
        headers = {'Content-Type': 'application/json', 'X-Auth-Method': 'OAUTH', 'X-Auth-Token': str(self.br_client.raw_token_results['access_token'])}
        url = self.br_client.dsp_host + "/traffic/sitelists"
        url = url + "/" + str(cid)
    
        result = requests.get(url, headers=headers)
        traffic_type = result.json()
        try:
            if traffic_type['errors']['httpStatusCode'] == 401:
                refresh_results_json = self.br_client.refresh_access_token()
        except:
            print("expected result")
        return traffic_type

    def update(self, cid, lists):
        headers = {'Content-Type': 'application/json', 'X-Auth-Method': 'OAUTH', 'X-Auth-Token': str(self.raw_token_results['access_token'])}
        r = requests.put(self.dsp_host + "/traffic/sitelists/" + str(cid), data=lists, headers=headers)
        results = r.json()
        try:
            if results['errors']['httpStatusCode'] == 401:
                refresh_results_json = self.refresh_access_token()
        except:
            print("expected result")
    
        return r

    def create(self, s_type, lists):
        headers = {'Content-Type': 'application/json', 'X-Auth-Method': 'OAUTH', 'X-Auth-Token': str(self.raw_token_results['access_token'])}
        r = requests.post(self.dsp_host + "/traffic/sitelists" , data=lists, headers=headers)
        results = r.json()
        try:
            if results['errors']['httpStatusCode'] == 401:
                refresh_results_json = self.refresh_access_token()
        except:
            print("expected result")
        return r

class Contextual:
    id = None
    name = None
    accountId = 0
    br_client = None
    taxonomyType = None
    categories = {
        "categories": [
            {
                "categoryId": 0
            },
        ]
    }
    updatedAt = None
    
    def __init__(self, br_client):
        self.br_client = br_client

    def read_by_id(self, cid):
        headers = {'Content-Type': 'application/json', 'X-Auth-Method': 'OAUTH', 'X-Auth-Token': str(self.br_client.raw_token_results['access_token'])}
        url = self.br_client.dsp_host + "/traffic/contextuals"
        url = url + "/" + str(cid)
    
        result = requests.get(url, headers=headers)
        traffic_type = result.json()
        try:
            if traffic_type['errors']['httpStatusCode'] == 401:
                refresh_results_json = self.br_client.refresh_access_token()
        except:
            print("expected result")
        return traffic_type

    def update(self, cid, lists):
        headers = {'Content-Type': 'application/json', 'X-Auth-Method': 'OAUTH', 'X-Auth-Token': str(self.raw_token_results['access_token'])}
        r = requests.put(self.dsp_host + "/traffic/contextuals/" + str(cid), data=lists, headers=headers)
        results = r.json()
        try:
            if results['errors']['httpStatusCode'] == 401:
                refresh_results_json = self.refresh_access_token()
        except:
            print("expected result")
    
        return r

    def create(self, s_type, lists):
        headers = {'Content-Type': 'application/json', 'X-Auth-Method': 'OAUTH', 'X-Auth-Token': str(self.raw_token_results['access_token'])}
        r = requests.post(self.dsp_host + "/traffic/contextuals" , data=lists, headers=headers)
        results = r.json()
        try:
            if results['errors']['httpStatusCode'] == 401:
                refresh_results_json = self.refresh_access_token()
        except:
            print("expected result")
        return r
        
    

class BrightRollClient:
  client_id = None
  client_secret = None
  id_host = None
  dsp_host = None
  request_auth_url = None
  yahoo_auth = None
  raw_token_results = None
  refresh_token = None
  token = None
  current_url = ''
  report_url = ''
  customerReportId = ''
  report_results_url = ''
  headers = None
  curl_url = None
  payload = ''

  def __init__(self, client_id='', client_secret='', id_host='', dsp_host=''):
    if len(client_id) == 0:
        try:
            self.client_id = os.environ['BR_CLIENT_ID']
            self.client_secret = os.environ['BR_CLIENT_SECRET']
            self.id_host = os.environ['BR_ID_HOST']
            self.dsp_host = os.environ['BR_DSP_HOST']
        except KeyError, e:
            print("Key error: {}".format(e.message))
            print("Missing environment variables. Be sure to assign values to:")
            print("apiclient.client_id")
            print("apiclient.client_secret")
            print("apiclient.id_host")
            print("apiclient.dsp_host")
    else:
        self.client_id = client_id
        self.client_secret = client_secret
        self.id_host = id_host
        self.dsp_host = dsp_host
         
    self.request_auth_url = self.id_host + "/oauth2/request_auth?client_id=" + self.client_id + "&redirect_uri=oob&response_type=code&language=en-us"
    self.current_url = ''
    self.report_url = 'https://api-sched-v3.admanagerplus.yahoo.com/yamplus_api/extreport/'
    try:
        self.refresh_token = os.environ['BR_REFRESH_TOKEN']
        self.raw_token_results = {}
        self.raw_token_results['refresh_token'] = os.environ['BR_REFRESH_TOKEN']
    except KeyError as e:
        print("error missing:")
        print(e)

  def set_refresh_token(self, refresh_token):
      self.refresh_token = refresh_token
      self.raw_token_results = {}
      self.raw_token_results['refresh_token'] = refresh_token
      return self.refresh_token

  def debug_curl(self, http_type='GET'):
      print('--- debug_curl ---')
      print(self.headers)
      print(self.curl_url)
      print(self.payload)
      print('--- debug_curl ---')
      
      # convert to cURL
      # exampli gratia: 
      # curl -X PUT https://api.one.aol.com/advertiser/inventory-management/v1/organizations/7000095690/advertisers/7000095690/whitelists  -H 'x-api-key: XlcRtA3hxcTDxwBvT3Nv9ra0BwPHxLe4N9xYYNn7' -H 'Content-Type: application/json' -H 'Authorization: Bearer a9d2241f-e2bb-4ec5-a758-67ca30924211' -d "{\"path\": \"/name\", \"value\": \"updated whitelist - 2017-12-06 15:10:11.225349\", \"op\": \"REPLACE\"}"
      curl_command = "curl -X " + http_type + " " + self.curl_url + " "
      # loop through headers to create headers string
      s_headers = ''
      for key,val in self.headers.items():
        s_headers = s_headers + "-H '{}: {}' ".format(key, val)
      curl_command = curl_command + s_headers
      if http_type != 'GET':
          curl_command = curl_command + '-d ' + self.payload

      print(curl_command)
      return curl_command

  def get_yahoo_auth_url(self):
    print("Go to this URL:")
    print(self.request_auth_url)

  def set_yahoo_auth(self, s_auth):
    self.yahoo_auth = s_auth
    return self.yahoo_auth

  def base64auth(self):
    return base64.b64encode((self.client_id + ":" + self.client_secret).encode())
    
  def get_access_token_json(self):
    get_token_url = self.id_host + "/oauth2/get_token"
    # payload = {'grant_type':'authorization_code', 'redirect_uri':'oob','code':self.yahoo_auth}
    payload = "grant_type=authorization_code&redirect_uri=oob&code=" + self.yahoo_auth
    # headers = {'Content-Type': 'application/json', 'Authorization': "Basic " + self.base64auth()}
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': "Basic " + self.base64auth().decode('utf-8')}
            
    print(get_token_url)
    print(payload)
    print(headers)
    # r = requests.post(get_token_url, json=payload, headers=headers)
    r = requests.post(get_token_url, data=payload, headers=headers)
    results_json = r.json()
    return results_json

  def refresh_access_token(self):
    get_token_url = self.id_host + "/oauth2/get_token"
    try:
        payload = "grant_type=refresh_token&redirect_uri=oob&refresh_token=" + self.raw_token_results['refresh_token'].encode('utf-8')
    except:
        payload = "grant_type=refresh_token&redirect_uri=oob&refresh_token=" + self.raw_token_results['refresh_token']
        
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': "Basic " + self.base64auth().decode('utf-8')}
    r = requests.post(get_token_url, data=payload, headers=headers)
    results_json = r.json()
    self.raw_token_results = r.json()
    self.refresh_token = self.raw_token_results['refresh_token']
    return results_json

  def cli_auth_dance(self):
    self.get_yahoo_auth_url()
    if sys.version_info < (3, 0):
      self.yahoo_auth = raw_input("Enter Yahoo! auth code: ")
    else:
      self.yahoo_auth = input("Enter Yahoo! auth code: ")

    print("Auth code, {}, entered.".format(self.yahoo_auth))
    self.raw_token_results = self.get_access_token_json()
    print("raw_token_results:")
    print(self.raw_token_results)
    self.refresh_token = self.raw_token_results['refresh_token']
    print("refresh_token:")
    print(self.refresh_token)

  #
  #
  # traffic types
  #
  #

  # {'errors': {'httpStatusCode': 401, 'message': 'HTTP 401 Unauthorized', 'validationErrors': []}, 'response': None, 'timeStamp': '2017-08-24T20:22:48Z'}
  def traffic_types(self, s_type):
    headers = {'Content-Type': 'application/json', 'X-Auth-Method': 'OAUTH', 'X-Auth-Token': str(self.raw_token_results['access_token'])}
    url = self.dsp_host + "/traffic/" + str(s_type)
    results = requests.get(url, headers=headers)
    types = results.json()
    try:
        if types['errors']['httpStatusCode'] == 401:
            refresh_results_json = self.refresh_access_token()
    except:
        print("expected result")
    return types

  # Works for s_types:
  # advertisers, campaigns, lines
  def traffic_type_by_id(self, s_type, cid):
    headers = {'Content-Type': 'application/json', 'X-Auth-Method': 'OAUTH', 'X-Auth-Token': str(self.raw_token_results['access_token'])}
    self.headers = headers
    url = self.dsp_host + "/traffic/" + str(s_type)
    url = url + "/" + str(cid)
    self.curl_url = url
    self.debug_curl()
    
    result = requests.get(url, headers=headers)
    traffic_type = result.json()
    try:
        if traffic_type['errors']['httpStatusCode'] == 401:
            refresh_results_json = self.refresh_access_token()
    except:
        print("expected result")
    return traffic_type

  # TODO:
  # do not pass to the results string if not set on our end
  def traffic_types_by_filter(self, s_type, account_id, page=0, limit=0, sort='', direction='asc', query=''):
    headers = {'Content-Type': 'application/json', 'X-Auth-Method': 'OAUTH', 'X-Auth-Token': str(self.raw_token_results['access_token'])}
    url = self.dsp_host + "/traffic/" + str(s_type)
    if s_type == 'lines':
        url = url + "?orderId=" + str(account_id)
    else:
        url = url + "?accountId=" + str(account_id)
        
    if page > 0:
        url = url + "&page=" + str(page)
    if limit > 0:
        url = url + "&limit=" + str(limit)
    if sort != '':
        url = url + "&sort=" + str(sort)
    if query != '':
        url = url + "&query=" + str(query)
    url = url + "&dir=" + str(direction)

    results = requests.get(url, headers=headers)

    traffic_types = results.json()
    try:
        if traffic_types['errors']['httpStatusCode'] == 401:
            refresh_results_json = self.refresh_access_token()
    except:
        print("expected result")
    return traffic_types
    
  def update_traffic_type(self, s_type, cid, payload):
    headers = {'Content-Type': 'application/json', 'X-Auth-Method': 'OAUTH', 'X-Auth-Token': str(self.raw_token_results['access_token'])}
    r = requests.put(self.dsp_host + "/traffic/" + str(s_type) + "/" + str(cid), data=payload, headers=headers)
    results = r.json()
    self.headers = headers
    self.payload = payload
    self.curl_url = self.dsp_host + "/traffic/" + str(s_type) + "/" + str(cid)
    self.debug_curl('PUT')
    print(results)
    try:
        if results['errors']['httpStatusCode'] == 401:
            refresh_results_json = self.refresh_access_token()
    except:
        print("expected result")
    
    return results

  def create_traffic_type(self, s_type, payload):
    headers = {'Content-Type': 'application/json', 'X-Auth-Method': 'OAUTH', 'X-Auth-Token': str(self.raw_token_results['access_token'])}
    r = requests.post(self.dsp_host + "/traffic/" + str(s_type) , data=payload, headers=headers)
    results = r.json()
    try:
        if results['errors']['httpStatusCode'] == 401:
            refresh_results_json = self.refresh_access_token()
    except:
        print("expected result")
    return results

  def create_report(self, reportOption, intervalTypeId, dateTypeId, startDate, endDate):
    headers = {'Content-Type': 'application/json', 'X-Auth-Method': 'OAUTH', 'X-Auth-Token': str(self.raw_token_results['access_token'])}
    payload = {"reportOption": reportOption, "intervalTypeId": intervalTypeId, "dateTypeId": dateTypeId, "startDate": startDate, "endDate": endDate}
    print('--- payload ---')
    print(payload)
    print('--- payload ---')

    print('--- headers ---')
    print(headers)
    print('--- headers ---')

    r = requests.post(self.report_url, data=str(payload).replace("'",'"'), headers=headers)
    print(self.report_url)
    print(r)
    print(r.json())
    results = r.json()
    try:
        if results['errors']['httpStatusCode'] == 401:
            refresh_results_json = self.refresh_access_token()
    except:
        print("expected result")
    self.customerReportId = results['customerReportId']
    return r
    
  def extract_report(self):
    self.headers = {'Content-Type': 'application/json', 'X-Auth-Method': 'OAUTH', 'X-Auth-Token': str(self.raw_token_results['access_token'])}
    results = requests.get(self.report_url + self.customerReportId, headers=self.headers)
    self.curl_url = self.report_url + self.customerReportId
    self.debug_curl()

    r = results.json()
    try:
        if r['errors']['httpStatusCode'] == 401:
            refresh_results_json = self.refresh_access_token()
    except:
        print("expected result")
    print('--- extracted report json ---')
    print(r)
    print('--- extracted report json ---')
    try:
        self.report_results_url = r['url']
    except:
        self.report_results_url = ''

    try:
        validationMessages = r['validationMessages']
        if validationMessages[0]['message'] == 'Requests Per Minute (RPM) limit reached. Please try again later.':
            print('return rate limit message')
            return validationMessages[0]['message']
            
    except:
        print('no sleep')
        
    return self.report_results_url
    
