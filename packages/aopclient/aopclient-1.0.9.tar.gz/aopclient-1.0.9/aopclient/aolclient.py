#!/usr/bin/env python

from future.standard_library import install_aliases
install_aliases()


import json
import jwt
import requests
import time
import os
import urllib3
import sys
from urllib3._collections import HTTPHeaderDict



use_environment_variables = None

try:
    from django.conf import settings
except ImportError:
    use_environment_variables = True


class AOLClient:
  client_id = None
  client_secret = None
  api_key = None
  id_host = None
  one_host = None
  aud = None
  payload = None
  encoded_payload = None
  oauth_url = None
  payload_url = None
  headers = None
  authorized_headers = None
  token = None
  curl_conversion = None


  def __init__(self):
    self.client_id = os.environ['AOP_CLIENT_ID']
    self.client_secret = os.environ['AOP_CLIENT_SECRET']
    self.api_key = os.environ['AOP_API_KEY']
    self.id_host = os.environ['AOP_ID_HOST']
    self.one_host = os.environ['AOP_ONE_HOST']

  def connect(self):
    self.set_payload()
    self.encode_payload()
    self.set_oauth_url()
    self.set_payload_url()
    self.set_headers()
    return self.get_token()

  def show_config(self):
    print(self.client_id)
    print(self.client_secret)
    print(self.api_key)
    print(self.id_host)
    print(self.one_host)


  def set_payload(self):
    now = int(time.time())
    self.payload = {
      "aud": "https://{0}/identity/oauth2/access_token?realm=aolcorporate/aolexternals".format(self.id_host),
      "iss": self.client_id,
      "sub": self.client_id,
      "exp": now + 3600,
      "iat": now ,
    }
    return self.payload

  def encode_payload(self):
    self.encoded_payload = jwt.encode(self.payload, self.client_secret, algorithm='HS256')
    return self.encoded_payload


  def set_oauth_url(self):
    self.oauth_url = "https://{0}/identity/oauth2/access_token".format(self.id_host)

  def set_payload_url(self):
    self.payload_url = "grant_type=client_credentials&scope=one&realm=aolcorporate/aolexternals&client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer&client_assertion={0}".format(bytes.decode(self.encoded_payload))
    return self.payload_url

  def set_headers(self):
    self.headers = {
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "application/json"
    }

  def get_token(self):
    response = self._send_request(self.oauth_url, self.headers, method="POST", data=self.payload_url)
    json_response = json.loads(response.text)
    print(json_response)
    self.token = json_response['access_token']
    # self.authorized_headers = {'Authorization': "Bearer " + self.token.encode('ascii')}
    self.authorized_headers = {'Authorization': "Bearer " + self.token}

    self.authorized_headers['Content-Type'] = 'application/json'
    self.authorized_headers['x-api-key'] = self.api_key

  def get_organizations(self):
    url = "https://{0}/advertiser/organization-management/v1/organizations/".format(self.one_host)
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def get_organization(self, id):
    url = "https://{0}/advertiser/organization-management/v1/organizations/{1}".format(self.one_host, id)
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)
      

  def get_advertisers(self, org_id=0):
    url = "https://{0}/advertiser/advertiser-management/v1/organizations/{1}/advertisers".format(self.one_host, org_id)
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def get_advertiser(self, org_id=0, ad_id=0):
    url = "https://{0}/advertiser/advertiser-management/v1/organizations/{1}/advertisers/{2}".format(self.one_host, org_id, ad_id)
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def get_campaigns(self, org_id=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/campaigns".format(self.one_host, org_id)
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def get_campaigns_by_advertiser(self, org_id=0, ad_id=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns".format(self.one_host, org_id, ad_id)
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def get_campaigns_by_advertiser_by_campaign(self, org_id=0, ad_id=0, campaign_id=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}".format(self.one_host, org_id, ad_id, campaign_id)
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def get_tactics_by_campaign(self, org_id=0, ad_id=0, campaign_id=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics".format(self.one_host, org_id, ad_id, campaign_id)
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def get_tactic_by_id(self, org_id=0, ad_id=0, campaign_id=0, tactic_id=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}".format(self.one_host, org_id, ad_id, campaign_id, tactic_id)
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def get_creative_assignments(self, org_id=0, ad_id=0, campaign_id=0, tactic_id=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}/creativeassignments".format(self.one_host, org_id, ad_id, campaign_id, tactic_id)
    response = self._send_request(url, self.authorized_headers, method="GET")
    print("{}".format(json.loads(response.text)))
    return json.loads(response.text)

  def get_deal_assignments(self, org_id=0, ad_id=0, campaign_id=0, tactic_id=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}/dealassignments".format(self.one_host, org_id, ad_id, campaign_id, tactic_id)
    response = self._send_request(url, self.authorized_headers, method="GET")
    print("{}".format(json.loads(response.text)))
    return json.loads(response.text)

  def assign_deal_assignments(self, org_id=0, ad_id=0, campaign_id=0, tactic_id=0, deals=[]):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}/dealassignments".format(self.one_host, org_id, ad_id, campaign_id, tactic_id)
    deal_data = []
    for deal in deals:
      deal_data.append(deal)
    response = self._send_request(url, self.authorized_headers, method="POST", data=json.dumps(deal_data))
    print("{}".format(json.loads(response.text)))
    return json.loads(response.text)

  def unassign_deal_assignments(self, org_id=0, ad_id=0, campaign_id=0, tactic_id=0, deals=[]):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}/dealassignments".format(self.one_host, org_id, ad_id, campaign_id, tactic_id)
    data = HTTPHeaderDict()
    for deal in deals:
        data.add('dealAssignmentId', str(deal))    
    response = self._send_request(url, self.authorized_headers, method="DELETE", data=data)
    print("{}".format(json.loads(response.text)))
    return json.loads(response.text)


  def get_flight_by_id(self, org_id=0, ad_id=0, campaign_id=0, tactic_id=0, flight_id=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}/flights/{5}".format(self.one_host, org_id, ad_id, campaign_id, tactic_id, flight_id)
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)


  def get_flights_by_tactic_id(self, org_id=0, ad_id=0, campaign_id=0, tactic_id=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}/flights".format(self.one_host, org_id, ad_id, campaign_id, tactic_id)
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def get_private_deals_by_advertiser(self, org_id=0, ad_id=0, limit=0, offset=0):
    url = "https://{0}/advertiser/inventory-management/v1/organizations/{1}/advertisers/{2}/deals".format(self.one_host, org_id, ad_id)
    if limit > 0 or offset > 0:
        url = url + "?limit={0}&offset={1}".format(limit, offset)        
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def get_private_deal_assignments_by_tactic(self, org_id=0, ad_id=0, campaign_id=0, tactic_id=0, limit=0, offset=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}/dealassignments".format(self.one_host, org_id, ad_id, campaign_id, tactic_id, limit, offset)
    if limit > 0 or offset > 0:
        url = url + "?limit={0}&offset={1}".format(limit, offset)        
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def get_blacklists_by_advertiser(self, org_id=0, ad_id=0, limit=0, offset=0):
    url = "https://{0}/advertiser/inventory-management/v1/organizations/{1}/advertisers/{2}/blacklists".format(self.one_host, org_id, ad_id, limit, offset)
    if limit > 0 or offset > 0:
        url = url + "?limit={0}&offset={1}".format(limit, offset)        
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def create_blacklist_by_advertiser(self, org_id=0, ad_id=0, name='', domains=[], apps=[], default=False):
    url = "https://{0}/advertiser/inventory-management/v1/organizations/{1}/advertisers/{2}/blacklists".format(self.one_host, org_id, ad_id)
    data = {}
    data['name'] = name
    data['domains'] = domains
    data['apps'] = apps
    data['default'] = default
    response = self._send_request(url, self.authorized_headers, method="POST", data=json.dumps(data))
    return json.loads(response.text)

  def update_blacklist_by_advertiser(self, org_id=0, ad_id=0, blacklist_id=0, op='REPLACE', path='/name', value=''):
    url = "https://{0}/advertiser/inventory-management/v1/organizations/{1}/advertisers/{2}/blacklists/{3}".format(self.one_host, org_id, ad_id, blacklist_id)
    data = {}
    data['op'] = op
    data['path'] = path
    data['value'] = value
    data_list = []
    data_list.append(data)
    response = self._send_request(url, self.authorized_headers, method="PATCH", data=json.dumps(data_list))
    return json.loads(response.text)
    
  def update_tactics_blacklist(self, org_id=0, ad_id=0, cammpaign_id=0, tactic_id=0, blacklist_id=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}/blacklists".format(self.one_host, org_id, ad_id, campaign_id, tactic_id)
    data = {}
    data['blacklistid'] = blacklist_id
    response = self._send_request(url, self.authorized_headers, method="PUT", data=data)

  def get_blacklists_by_tactic(self, org_id=0, ad_id=0, campaign_id=0, tactic_id=0, limit=0, offset=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}/blacklists".format(self.one_host, org_id, ad_id, campaign_id, tactic_id, limit, offset)
    if limit > 0 or offset > 0:
        url = url + "?limit={0}&offset={1}".format(limit, offset)        
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def get_domains_by_blacklist(self, org_id=0, ad_id=0, blacklist_id=0, limit=0, offset=0):
    url = "https://{0}/advertiser/inventory-management/v1/organizations/{1}/advertisers/{2}/blacklists/{3}/domains".format(self.one_host, org_id, ad_id, blacklist_id, limit, offset)
    if limit > 0 or offset > 0:
        url = url + "?limit={0}&offset={1}".format(limit, offset)        
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)
      
  def get_domains_by_whitelist(self, org_id=0, ad_id=0, whitelist_id=0, limit=0, offset=0):
    url = "https://{0}/advertiser/inventory-management/v1/organizations/{1}/advertisers/{2}/blacklists/{3}/domains".format(self.one_host, org_id, ad_id, whitelist_id, limit, offset)
    if limit > 0 or offset > 0:
        url = url + "?limit={0}&offset={1}".format(limit, offset)        
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def get_whitelists_by_tactic(self, org_id=0, ad_id=0, campaign_id=0, tactic_id=0, limit=0, offset=0):      
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}/whitelists".format(self.one_host, org_id, ad_id, campaign_id, tactic_id, limit, offset)
    if limit > 0 or offset > 0:
        url = url + "?limit={0}&offset={1}".format(limit, offset)        
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def get_whitelists_by_advertiser(self, org_id=0, ad_id=0, limit=0, offset=0):
    url = "https://{0}/advertiser/inventory-management/v1/organizations/{1}/advertisers/{2}/whitelists".format(self.one_host, org_id, ad_id, limit, offset)
    if limit > 0 or offset > 0:
        url = url + "?limit={0}&offset={1}".format(limit, offset)        
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def create_whitelist_by_advertiser(self, org_id=0, ad_id=0, name='', domains=[], apps=[], default=False):
    url = "https://{0}/advertiser/inventory-management/v1/organizations/{1}/advertisers/{2}/whitelists".format(self.one_host, org_id, ad_id)
    data = {}
    data['name'] =  name
    data['domains'] = domains
    data['apps'] = apps
    data['default'] = default
    response = self._send_request(url, self.authorized_headers, method="POST", data=json.dumps(data))
    return json.loads(response.text)

  def update_whitelist_by_advertiser(self, org_id=0, ad_id=0, whitelist_id=0, op='REPLACE', path='/name', value=''):
    url = "https://{0}/advertiser/inventory-management/v1/organizations/{1}/advertisers/{2}/whitelists/{3}".format(self.one_host, org_id, ad_id, whitelist_id)
    data = {}
    data['op'] = op
    data['path'] = path
    data['value'] = value
    data_list = []
    data_list.append(data)
    response = self._send_request(url, self.authorized_headers, method="PATCH", data=json.dumps(data_list))
    return json.loads(response.text)

  def update_tactics_whitelist(self, org_id=0, ad_id=0, cammpaign_id=0, tactic_id=0, whitelist_id=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}/whitelists".format(self.one_host, org_id, ad_id, campaign_id, tactic_id)
    data = {}
    data['whitelistid'] = whitelist_id
    response = self._send_request(url, self.authorized_headers, method="PUT", data=json.dump(data))

  def get_apps_by_whitelist(self, org_id=0, ad_id=0, whitelist_id=0, limit=0, offset=0):
    url = "https://{0}/advertiser/inventory-management/v1/organizations/{1}/advertisers/{2}/whitelists/{3}/apps".format(self.one_host, org_id, ad_id, whitelist_id, limit, offset)
    if limit > 0 or offset > 0:
        url = url + "?limit={0}&offset={1}".format(limit, offset)        
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def get_creatives_by_tactic(self, org_id=0, ad_id=0, campaign_id=0, tactic_id=0, limit=0, offset=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}/creativeassignments".format(self.one_host, org_id, ad_id, campaign_id, tactic_id, limit, offset)
    if limit > 0 or offset > 0:
        url = url + "?limit={0}&offset={1}".format(limit, offset)        
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def get_inventory_sources_by_tactic(self, org_id=0, ad_id=0, campaign_id=0, tactic_id=0, limit=0, offset=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}/inventorysources".format(self.one_host, org_id, ad_id, campaign_id, tactic_id, limit, offset)
    if limit > 0 or offset > 0:
        url = url + "?limit={0}&offset={1}".format(limit, offset)        
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def get_avails_by_tactic(self, org_id=0, ad_id=0, campaign_id=0, tactic_id=0, limit=0, offset=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}/availableinventorysources".format(self.one_host, org_id, ad_id, campaign_id, tactic_id, limit, offset)
    if limit > 0 or offset > 0:
        url = url + "?limit={0}&offset={1}".format(limit, offset)        
    response = self._send_request(url, self.authorized_headers, method="GET")
    return json.loads(response.text)

  def update_inventory_sources_by_tactic(self, org_id=0, ad_id=0, campaign_id=0, tactic_id=0, dsp_ids=[], limit=0, offset=0):
    url = "https://{0}/advertiser/campaign-management/v1/organizations/{1}/advertisers/{2}/campaigns/{3}/tactics/{4}/inventorysources".format(self.one_host, org_id, ad_id, campaign_id, tactic_id, limit, offset)
    data = dsp_ids
    if limit > 0 or offset > 0:
        url = url + "?limit={0}&offset={1}".format(limit, offset)        
    response = self._send_request(url, self.authorized_headers, method="PUT", data=json.dumps(data))
    return json.loads(response.text)

  def _convert_to_curl(self, method, url, headers, data):
    curl_conversion = "curl -X {} {} ".format(method, url) 
    if sys.version_info < (3, 0):
      for key, value in headers.iteritems():
        curl_conversion = curl_conversion + " -H '{}: {}'".format(key, value)
    else: 
      for key, value in headers.items():
        curl_conversion = curl_conversion + " -H '{}: {}'".format(key, value)
    curl_conversion = curl_conversion + " -d " + "{}".format(json.dumps(data))
    return curl_conversion
      
  def _send_request(self, url, headers, data=None, method="GET"):
      response = None
      self.curl_conversion = self._convert_to_curl(method, url, headers, data)
      print('--- self.curl_conversion ---')
      print(self.curl_conversion)
      print('--- self.curl_conversion ---')
      if method == "GET":
          response = requests.get(url, headers=headers, verify=True)

      if method == "DELETE":
          response = requests.delete(url, headers=headers, verify=True, data=data)

      if method == "POST":
          response = requests.post(url, headers=headers, verify=True, data=data)
          print('--- headers ---')
          print(headers)
          print('--- headers ---')
          print('--- data ---')
          print(data)
          print('--- data ---')

      if method == "PUT":
          response = requests.put(url, headers=headers, verify=True, data=data)
          print('--- headers ---')
          print(headers)
          print('--- headers ---')
          print('--- data ---')
          print(data)
          print('--- data ---')
          print('--- url ---')
          print(url)
          print('--- url ---')

      if method == "PATCH":
          response = requests.patch(url, headers=headers, verify=True, data=data)

      print('--- response.status_code: {} ---'.format(response.status_code))
      codes = [200,201]
      if (response.status_code in codes) != True:
          message = ""
          try:
              message = json.loads(response.text)['message']
          except:
              # cant get message
              pass

          raise Exception("Bad Response from AOP. Status Code: {status_code} -- Message: {message}".format(
                  status_code=str(response.status_code),
                  message=message))

      return response
# eof
