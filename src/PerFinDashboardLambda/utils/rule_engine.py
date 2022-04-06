import re
class RuleEngine:
	COMMAND_DELIMITER = "%%"
	def Regex(self,left,right):
		paramVal = self.entry[left]
		print(right)
		print(left)
		print(paramVal)
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


	def __init__(self,rules):
		self.operationMap = {
		 'REGEX': self.Regex,
		 'OR' : self.Or,
		 'AND': self.And
		}
		self.rules = rules
		self.entry = None

	def _match(self,sub_rule):
		print(sub_rule)
		rule_components = self.rules[sub_rule].split(RuleEngine.COMMAND_DELIMITER)
		left = rule_components[0]
		right = rule_components[2]
		operation = rule_components[1]
		print(rule_components)
		return self.operationMap[operation](left,right)

	def match(self,entry):
		print(entry)
		self.entry = entry
		return self._match('root')
