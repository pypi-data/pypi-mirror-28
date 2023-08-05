# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
class QueryDomainListRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Domain', '2016-05-11', 'QueryDomainList')

	def get_ProductDomainType(self):
		return self.get_query_params().get('ProductDomainType')

	def set_ProductDomainType(self,ProductDomainType):
		self.add_query_param('ProductDomainType',ProductDomainType)

	def get_RegStartDate(self):
		return self.get_query_params().get('RegStartDate')

	def set_RegStartDate(self,RegStartDate):
		self.add_query_param('RegStartDate',RegStartDate)

	def get_OrderKeyType(self):
		return self.get_query_params().get('OrderKeyType')

	def set_OrderKeyType(self,OrderKeyType):
		self.add_query_param('OrderKeyType',OrderKeyType)

	def get_GroupId(self):
		return self.get_query_params().get('GroupId')

	def set_GroupId(self,GroupId):
		self.add_query_param('GroupId',GroupId)

	def get_DeadEndDate(self):
		return self.get_query_params().get('DeadEndDate')

	def set_DeadEndDate(self,DeadEndDate):
		self.add_query_param('DeadEndDate',DeadEndDate)

	def get_DomainName(self):
		return self.get_query_params().get('DomainName')

	def set_DomainName(self,DomainName):
		self.add_query_param('DomainName',DomainName)

	def get_StartDate(self):
		return self.get_query_params().get('StartDate')

	def set_StartDate(self,StartDate):
		self.add_query_param('StartDate',StartDate)

	def get_PageNum(self):
		return self.get_query_params().get('PageNum')

	def set_PageNum(self,PageNum):
		self.add_query_param('PageNum',PageNum)

	def get_OrderByType(self):
		return self.get_query_params().get('OrderByType')

	def set_OrderByType(self,OrderByType):
		self.add_query_param('OrderByType',OrderByType)

	def get_RegEndDate(self):
		return self.get_query_params().get('RegEndDate')

	def set_RegEndDate(self,RegEndDate):
		self.add_query_param('RegEndDate',RegEndDate)

	def get_EndDate(self):
		return self.get_query_params().get('EndDate')

	def set_EndDate(self,EndDate):
		self.add_query_param('EndDate',EndDate)

	def get_DomainType(self):
		return self.get_query_params().get('DomainType')

	def set_DomainType(self,DomainType):
		self.add_query_param('DomainType',DomainType)

	def get_DeadStartDate(self):
		return self.get_query_params().get('DeadStartDate')

	def set_DeadStartDate(self,DeadStartDate):
		self.add_query_param('DeadStartDate',DeadStartDate)

	def get_UserClientIp(self):
		return self.get_query_params().get('UserClientIp')

	def set_UserClientIp(self,UserClientIp):
		self.add_query_param('UserClientIp',UserClientIp)

	def get_PageSize(self):
		return self.get_query_params().get('PageSize')

	def set_PageSize(self,PageSize):
		self.add_query_param('PageSize',PageSize)

	def get_Lang(self):
		return self.get_query_params().get('Lang')

	def set_Lang(self,Lang):
		self.add_query_param('Lang',Lang)

	def get_QueryType(self):
		return self.get_query_params().get('QueryType')

	def set_QueryType(self,QueryType):
		self.add_query_param('QueryType',QueryType)