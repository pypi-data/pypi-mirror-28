import datetime
import hmac
import hashlib
import base64
import requests
import json


class mypoolin_imps(object):
	"""Class to access mypoolin_imps"""
	base_url = "https://hmacsdk.mypoolin.com/merchants_imps"

	def __init__(self, username, secret):
		super(mypoolin_upi, self).__init__()
		self.secret = secret
		self.username = username
	
	def __hmac_requests(self,req_type,endpoint,**kwargs):
		req = requests.Request(url=self.base_url+endpoint,data=kwargs)
		prepared = req.prepare()
		encoded_params = prepared.body
		strg = datetime.datetime.strftime(datetime.datetime.utcnow(),"%a, %d %b %Y %H:%M:%S ")+"GMT"
		resp = req
		if req_type == "POST":
			only_sha256 = hashlib.sha256(encoded_params).digest()
			request_body_digest = base64.b64encode(only_sha256)
			hashable_string = "date: "+strg+"\ndigest: SHA-256={}".format(request_body_digest)
			request_line_digest = hmac.new(self.secret,hashable_string,hashlib.sha256).digest()
			request_line_digest = base64.b64encode(request_line_digest)
			headers = {
				"date":strg,
				"authorization":'hmac username="{}",algorithm="hmac-sha256",headers="date digest",signature="{}"'.format(self.username,request_line_digest),
				"digest":"SHA-256={}".format(request_body_digest),
			}
			resp = requests.post(url=self.base_url+endpoint,data=kwargs,headers=headers)
		if req_type == "GET":
			only_sha256 = hashlib.sha256(encoded_params).digest()
			request_body_digest = base64.b64encode(only_sha256)
			hashable_string = "date: "+strg
			request_line_digest = hmac.new(self.secret,hashable_string,hashlib.sha256).digest()
			request_line_digest = base64.b64encode(request_line_digest)
			headers = {
				"date":strg,
				"authorization":'hmac username="{}",algorithm="hmac-sha256",headers="date",signature="{}"'.format(self.username,request_line_digest)
			}
			resp = requests.get(url=self.base_url+endpoint,data=kwargs,headers=headers)
		return resp
		
	def __json_validation_and_return(self,text):
		try:
			json_object = json.loads(text)
		except ValueError, e:
			return text
		return json.loads(text)

	def request_imps_single(self,beneficiary_account_number,beneficiary_ifsc_code,beneficiary_amount):
		resp = self.hmac_requests("POST","/request_imps_single",beneficiary_account_number=beneficiary_account_number,beneficiary_ifsc_code=beneficiary_ifsc_code,beneficiary_amount=beneficiary_amount)
		return self.json_validation_and_return(resp.text)

	def request_imps_single_async(self,beneficiary_account_number,beneficiary_ifsc_code,beneficiary_amount):
		resp = self.hmac_requests("POST","/request_imps_single_async",beneficiary_account_number=beneficiary_account_number,beneficiary_ifsc_code=beneficiary_ifsc_code,beneficiary_amount=beneficiary_amount)
		return self.json_validation_and_return(resp.text)

	def check_transaction_status(self,order_id):
		resp = self.hmac_requests("POST","/check_transaction_status",order_id=order_id)
		return self.json_validation_and_return(resp.text)

	def get_balance(self):
		resp = self.hmac_requests("GET","/get_balance")
		return self.json_validation_and_return(resp.text)


