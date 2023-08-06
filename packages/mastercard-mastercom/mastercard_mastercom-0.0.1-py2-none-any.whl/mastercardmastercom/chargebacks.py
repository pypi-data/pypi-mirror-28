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

class Chargebacks(BaseObject):
	"""
	
	"""

	__config = {
		
		"4542d6c4-e3c6-4c0b-a628-4f27d9d10df8" : OperationConfig("/mastercom/v1/claims/{claim-id}/chargebacks", "create", [], []),
		
		"a70d2a7f-31d6-4cf2-9c75-bd1f7ed2983d" : OperationConfig("/mastercom/v1/claims/{claim-id}/chargebacks/{chargeback-id}/reversal", "create", [], []),
		
		"2b0ce60e-c7f3-43d4-b096-6a4b5d5a19a5" : OperationConfig("/mastercom/v1/claims/{claim-id}/chargebacks/{chargeback-id}/documents", "query", [], ["chargeback-type","format"]),
		
		"3b81d1df-7a99-42ef-9c94-367354cab911" : OperationConfig("/mastercom/v1/claims/{claim-id}/chargebacks/loaddataforchargebacks", "query", [], []),
		
		"c18c92e6-1982-474b-87f6-177080b19c0f" : OperationConfig("/mastercom/v1/claims/{claim-id}/chargebacks/{chargeback-id}", "update", [], []),
		
	}

	def getOperationConfig(self,operationUUID):
		if operationUUID not in self.__config:
			raise Exception("Invalid operationUUID: "+operationUUID)

		return self.__config[operationUUID]

	def getOperationMetadata(self):
		return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative())


	@classmethod
	def create(cls,mapObj):
		"""
		Creates object of type Chargebacks

		@param Dict mapObj, containing the required parameters to create a new object
		@return Chargebacks of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("4542d6c4-e3c6-4c0b-a628-4f27d9d10df8", Chargebacks(mapObj))






	@classmethod
	def createReversal(cls,mapObj):
		"""
		Creates object of type Chargebacks

		@param Dict mapObj, containing the required parameters to create a new object
		@return Chargebacks of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("a70d2a7f-31d6-4cf2-9c75-bd1f7ed2983d", Chargebacks(mapObj))











	@classmethod
	def retrieveDocumentation(cls,criteria):
		"""
		Query objects of type Chargebacks by id and optional criteria
		@param type criteria
		@return Chargebacks object representing the response.
		@raise ApiException: raised an exception from the response status
		"""

		return BaseObject.execute("2b0ce60e-c7f3-43d4-b096-6a4b5d5a19a5", Chargebacks(criteria))






	@classmethod
	def getPossibleValueListsForCreate(cls,criteria):
		"""
		Query objects of type Chargebacks by id and optional criteria
		@param type criteria
		@return Chargebacks object representing the response.
		@raise ApiException: raised an exception from the response status
		"""

		return BaseObject.execute("3b81d1df-7a99-42ef-9c94-367354cab911", Chargebacks(criteria))


	def update(self):
		"""
		Updates an object of type Chargebacks

		@return Chargebacks object representing the response.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("c18c92e6-1982-474b-87f6-177080b19c0f", self)






