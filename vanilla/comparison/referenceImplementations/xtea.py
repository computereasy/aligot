#!/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------
# Aligot project
#
# Copyright, licence: who cares?
# ----------------------------------------------

import ciphers

import struct
from ctypes import *

class cipher(ciphers.cipherTemplate):

	'''
		Source: http://code.activestate.com/recipes/496737-python-xtea-encryption/
	'''

	def __init__(self):

		self._name = 'XTEA'
		self._plaintextLength = 8
		self._keyLength = 16
		self._ciphertextLength = 8
		self.hashFunction = False
		self._blacklistedValues = {'9e3779b9','c6ef3720','00000020'}

	def encipher(self, inputText, key):

		assert len(inputText) == 2*self._plaintextLength, "Bad parameter size for enciphering " + self._name
		
		n = 32
		endian = '!'
		
		encInputText = self._encode(inputText)
		encKey = self._encode(key)

		v0,v1 = struct.unpack(endian+"2L",encInputText)
		k = struct.unpack(endian+"4L",encKey)

		sum,delta,mask = 0L,0x9e3779b9L,0xffffffffL
		for round in range(n):
			v0 = (v0 + (((v1<<4 ^ v1>>5) + v1) ^ (sum + k[sum & 3]))) & mask
			sum = (sum + delta) & mask
			v1 = (v1 + (((v0<<4 ^ v0>>5) + v0) ^ (sum + k[sum>>11 & 3]))) & mask
	    
		return self._decode(struct.pack(endian+"2L",v0,v1))


	def decipher(self, inputText, key):

		assert len(inputText) == 2*self._ciphertextLength, "Bad parameter size for deciphering " + self._name

		n = 32
		endian = '!'
		delta=0x9e3779b9L

		encInputText = self._encode(inputText)
		encKey = self._encode(key)
		
		v0,v1 = struct.unpack(endian+"2L",encInputText)
		k = struct.unpack(endian+"4L",encKey)
		mask = 0xffffffffL
		sum = (delta * n) & mask

		for round in range(n):
			v1 = (v1 - (((v0<<4 ^ v0>>5) + v0) ^ (sum + k[sum>>11 & 3]))) & mask
			sum = (sum - delta) & mask
			v0 = (v0 - (((v1<<4 ^ v1>>5) + v1) ^ (sum + k[sum & 3]))) & mask
		
		return self._decode(struct.pack(endian+"2L",v0,v1))

	def _encode(self, inputText):

		return inputText.decode('hex')

	def _decode(self, inputText):

		return inputText.encode('hex')

	def isBlacklistedValue(self, val):

		return (val in self._blacklistedValues)

	def getName(self):

		return self._name

	def getPlaintextLength(self):

		return self._plaintextLength

	def getKeyLength(self):

		return self._keyLength

	def getCiphertextLength(self):

		return self._ciphertextLength

