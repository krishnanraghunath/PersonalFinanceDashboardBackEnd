import re
'''
Rules we are looking for operations done on accountring entry 
eg:
1. txnDessription contains USER@UPI this word and amount > 10K and txnType == CREDIT  ==> USER_HIGH_VAL_TXNS_CREDIT like that
Now how to define them and making it easier for user to define it. 
We can split them into sperate statements
A statement ==> Left%%Operation%%Right  -> staement processor should return true or false
What is Left and Right? It can be another statement or a parameters in ACCOUNT ENTRY (at the end we are categorizing an account entry)
Operation Left 									Right
REGEX     account entry param					Regex string
GT		  account entry param					amount 
LT		  account entry param					amount     
EQ		  account entry param					amount    
OR		  statement 	   						statement
AND		  statement 	   						statement
'''



class RuleEngine:
	COMMAND_DELIMITER = "%%"
	def Regex(self,left,right):
		paramVal = self.entry[left]
		return re.compile(right).search(paramVal) != None

	def Or(self,left,right):
		if self._match(left):
			return True
		if self._match(right):
			return True
		return False

	def And(self,left,right):
		if not self._match(left):
			return False
		if not self._match(right):
			return False
		return True

	def GT(self,left,right):
		try:
			paramVal = self.entry[left]
			if paramVal > right:
				return True
		except:
			return False
		return False

	def LT(self,left,right):
		try:
			paramVal = self.entry[left]
			if paramVal < right:
				return True
		except:
			return False
		return False

	def __init__(self,rules):
		self.operationMap = {
		 'REGEX': self.Regex,
		 'OR' : self.Or,
		 'AND': self.And
		}
		self.rules = rules
		self.entry = None

	def _match(self,sub_rule):
		if sub_rule not in self.rules:
			return False
		rule_components = self.rules[sub_rule]
		left = rule_components['lOperand']
		right = rule_components['rOperand']
		operation = rule_components['operation']
		return self.operationMap[operation](left,right)

	def match(self,entry):
		self.entry = entry
		return self._match('root')
