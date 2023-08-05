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
class QueryCustomMetricListRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Cms', '2017-03-01', 'QueryCustomMetricList','cms')

	def get_Size(self):
		return self.get_query_params().get('Size')

	def set_Size(self,Size):
		self.add_query_param('Size',Size)

	def get_GroupId(self):
		return self.get_query_params().get('GroupId')

	def set_GroupId(self,GroupId):
		self.add_query_param('GroupId',GroupId)

	def get_Page(self):
		return self.get_query_params().get('Page')

	def set_Page(self,Page):
		self.add_query_param('Page',Page)

	def get_MetricName(self):
		return self.get_query_params().get('MetricName')

	def set_MetricName(self,MetricName):
		self.add_query_param('MetricName',MetricName)

	def get_Dimension(self):
		return self.get_query_params().get('Dimension')

	def set_Dimension(self,Dimension):
		self.add_query_param('Dimension',Dimension)

	def get_UUID(self):
		return self.get_query_params().get('UUID')

	def set_UUID(self,UUID):
		self.add_query_param('UUID',UUID)

	def get_Md5(self):
		return self.get_query_params().get('Md5')

	def set_Md5(self,Md5):
		self.add_query_param('Md5',Md5)