#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#


from mastercardapicore import BaseObject
from mastercardapicore import RequestMap
from mastercardapicore import OperationConfig
from mastercardapicore import OperationMetadata
from resourceconfig import ResourceConfig

class Transactions(BaseObject):
	"""
	
	"""

	__config = {
		
		"0d5a8da9-c6f6-447e-b5f6-b2569891bfa2" : OperationConfig("/mastercom/v1/claims/{claim-id}/transactions/clearing/{transaction-id}", "read", [], []),
		
		"0cb03c8e-66a6-484f-8377-2c0157f61a19" : OperationConfig("/mastercom/v1/claims/{claim-id}/transactions/authorization/{transaction-id}", "read", [], []),
		
		"64487f68-4cae-4267-9c23-e9132829e797" : OperationConfig("/mastercom/v1/transactions/search", "create", [], []),
		
	}

	def getOperationConfig(self,operationUUID):
		if operationUUID not in self.__config:
			raise Exception("Invalid operationUUID: "+operationUUID)

		return self.__config[operationUUID]

	def getOperationMetadata(self):
		return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative())






	@classmethod
	def retrieveClearingDetail(cls,id,criteria=None):
		"""
		Returns objects of type Transactions by id and optional criteria
		@param str id
		@param dict criteria
		@return instance of Transactions
		@raise ApiException: raised an exception from the response status
		"""
		mapObj =  RequestMap()
		if id:
			mapObj.set("id", id)

		if criteria:
			if (isinstance(criteria,RequestMap)):
				mapObj.setAll(criteria.getObject())
			else:
				mapObj.setAll(criteria)

		return BaseObject.execute("0d5a8da9-c6f6-447e-b5f6-b2569891bfa2", Transactions(mapObj))






	@classmethod
	def retrieveAuthorizationDetail(cls,id,criteria=None):
		"""
		Returns objects of type Transactions by id and optional criteria
		@param str id
		@param dict criteria
		@return instance of Transactions
		@raise ApiException: raised an exception from the response status
		"""
		mapObj =  RequestMap()
		if id:
			mapObj.set("id", id)

		if criteria:
			if (isinstance(criteria,RequestMap)):
				mapObj.setAll(criteria.getObject())
			else:
				mapObj.setAll(criteria)

		return BaseObject.execute("0cb03c8e-66a6-484f-8377-2c0157f61a19", Transactions(mapObj))


	@classmethod
	def searchForTransaction(cls,mapObj):
		"""
		Creates object of type Transactions

		@param Dict mapObj, containing the required parameters to create a new object
		@return Transactions of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("64487f68-4cae-4267-9c23-e9132829e797", Transactions(mapObj))







