# ROPGenerator - Database.py module
# Storing the gadgets that are used during analysis 

import sys
from Analysis import *
from Gadget import *
from datetime import datetime


# List of the available gadgets 
gadgetDB = [] 

# exprLookUp
# class used to store dependencies of type EXPRtoREG
class exprLookUp:
	def __init__(self):
		self.expr_list = [] # LIst of EXPR that are stored in REG 
		self.gadget_list = [] # gadget_list[i] = list of gadgets that put expr_list[i] in the regiter 
		
	
	def lookUpEXPRtoREG(self, expr, n=10):
		i = 0
		found = 0
		res = []
		# Iterate for all write addresses 
		while( i < len(self.expr_list ) and len(res) < n):
			# Comparing the addresses with hard=True so we call z3 solver 
			cond = Cond(CT.EQUAL, self.expr_list[i], expr)
			if( cond.isTrue(hard=True)):
				res += self.gadget_list[i]
			i = i + 1
		return res 


# memLookUp:
# class used to help storing the dependencies for the memory in gadgetLookUp
class memLookUp:
	def __init__(self):
		self.addr_list=[] # To check if an access to an address is available
		self.written_values=[] # List of dictionnaries 
		# DIctionnary written_values[i] corresponds to values written at addr_list[i]
		# Depending on the use: 
		#	REGtoMEM : keys are register uid (int)
		#	CSTtoMEM : keys are the constant value (int)
		#	...
		
	def lookUpREGtoMEM( self, addr, reg, n=10 ):
		"""
		Returns gadgets numbers that put reg at mem(addr) as a list of gadgets uids 
		reg - (int)
		addr - Expr
		"""
		i = 0
		found = 0
		res = []
		# Iterate for all write addresses 
		while( i < len(self.addr_list ) and len(res) < n):
			# If we have a dependencie for the requested register 
			if( reg in self.written_values[i]):
				# Comparing the addresses with hard=True so we call z3 solver 
				cond = Cond(CT.EQUAL, self.addr_list[i], addr)
				if( cond.isTrue(hard=True)):
					res += self.written_values[i][reg]
			i = i + 1
		return res 
		
	def lookUpCSTtoMEM( self, addr, cst, n=10):
		"""
		Returns gadgets numbers that put cst at mem(addr) as a list of gadgets uids 
		cst - (int)
		addr - Expr
		"""
		i = 0
		found = 0
		res = []
		# Iterate for all write addresses 
		while( i < len(self.addr_list ) and len(res) < n):
			# If we have a dependencie for the requested register 
			if( cst in self.written_values[i]):
				# Comparing the addresses with hard=True so we call z3 solver 
				cond = Cond(CT.EQUAL, self.addr_list[i], addr)
				if( cond.isTrue(hard=True)):
					res += self.written_values[i][cst]
			i = i + 1
		return res 


# Hash tables to look up registers
# Different kinds :
# REGtoREG, REGtoMEM, MEMtoREG, MEMtoMEM, CSTtoREG, CSTtoMEM

# gadgetLookUp: 
# keys are GadgetTypes
# values are dictionnaries (different organization for all of them 

# REGtoREG dictionnary : gadgetLookUp[REGtoREG][REG1][REG2] = uid (number) of gadget in the gadgetDB list that puts REG2 in REG1 
# CSTtoREG dictionnary : gadgetLookUp[REGtoREG][REG][CST] = uid (number) of gadget in the gadgetDB list that puts CST in REG
# MEMtoREG dictionnary : gadgetLookUp[MEMtoREG][REG][ADDR] = uid (number) of gadget in the gadgetDB that puts MEM[addr] in REG 
# REGtoMEM dictionnary : gadgetLookUp[REGtoMEM] = memLookUp() for gadgets  that writes reg in the memory 
# CSTtoMEM dictionnary : gadgetLookUp[CSTtoMEM] = memLookUp() for gadgets that writes cst in the memory 
# EXPRtoREG dictionnary : gadgetLookUp[EXPRtoREG][REG] = exprLookUp() 
gadgetLookUp = {GadgetType.REGtoREG:dict(), GadgetType.REGtoMEM:memLookUp(), GadgetType.MEMtoREG:dict(),GadgetType.CSTtoREG:dict(),GadgetType.CSTtoMEM:memLookUp(), GadgetType.EXPRtoREG:dict()}


def generated_gadgets_to_DB():
	"""
	Generates the list of the available gadgets for ROP 
	Usage : must be called after the gadgets opcodes have been stored into the opcodes_gadget array in Generated_opcodes.py file.
	Result : 
		No value returned. But the gadgets are stored in the gadgets[] array in Database module.  
	"""
	
	 # List of all gadgets in assembly
	import Generated_opcodes
	asmGadgets = Generated_opcodes.opcodes_gadget
	
	i = 0
	success = 0
	startTime = datetime.now()
	chargingBarSize = 30
	chargingBarStr = " "*chargingBarSize
	sys.stdout.write("[+] Working under architecture: " + ArchInfo.currentArch + '\n')
	sys.stdout.write("[+] Creating gadget database : \n") 
	sys.stdout.write("\tProgression [")
	sys.stdout.write(chargingBarStr)
	sys.stdout.write("]\r\tProgression [")
	sys.stdout.flush()                       
	for g in asmGadgets:
		asm = g[1]
		addr = g[0]
		# DEBUG print("\\x"+ "\\x".join("{:02x}".format(ord(c)) for c in asm))
		try:
			if( i % (len(asmGadgets)/30) == 0 and i > 0 or i == len(asmGadgets)):
				sys.stdout.write("|")
				sys.stdout.flush()
			gadget = Gadget(i, addr, asm)
			success += 1
			gadgetDB.append( gadget )
		except GadgetException as e:
			#print e
			pass
		i += 1
	sys.stdout.write("\r"+" "*90+"\r")
		
	cTime = datetime.now() - startTime	
	print "\tGadgets analyzed : " + str(len(asmGadgets))
	print "\tSuccessfully translated : " + str(success)
	print "\tComputation time : " + str(cTime)
	
def fillGadgetLookUp():
	"""
	Fill the gadgetLookUp dictionnary with gadgets from the gadgetDB list 
	"""
	# Initialize the gadgetLookUp dictionnaries 
	# Only done for REGtoREG so far 
	for reg_num in revertRegNamesTable.keys():
		# For REGtoREG
		gadgetLookUp[GadgetType.REGtoREG][reg_num] = dict()
		for reg_num2 in revertRegNamesTable.keys():
			gadgetLookUp[GadgetType.REGtoREG][reg_num][reg_num2] = []
		# For CSTtoREG
		gadgetLookUp[GadgetType.CSTtoREG][reg_num] = dict()
		# For MEMtoREG
		gadgetLookUp[GadgetType.MEMtoREG][reg_num] = dict()
		# For REGtoMEM
		# No initialisation needed 
			
	
	# Update the gadgetLookUp table 
	for i in range(0, len(gadgetDB) ):
		gadget = gadgetDB[i]
		for reg, deps in gadget.getDependencies().regDep.iteritems():	
			for dep in deps:
				# For REGtoREG
				if( isinstance(dep[0], SSAExpr) and dep[1].isTrue()):
					gadgetLookUp[GadgetType.REGtoREG][reg.num][dep[0].reg.num].append(i)
				# For CSTtoREG
				elif( isinstance(dep[0], ConstExpr) and dep[1].isTrue()):
					if( not dep[0].value in gadgetLookUp[GadgetType.CSTtoREG][reg.num] ):
						gadgetLookUp[GadgetType.CSTtoREG][reg.num][dep[0].value] = [i]
					else:	
						gadgetLookUp[GadgetType.CSTtoREG][reg.num][dep[0].value].append(i)
				# For XXXtoREG
				elif( isinstance(dep[0], MEMExpr) and dep[1].isTrue() ):
					# For MEMtoREG
					if( isinstance(dep[0].addr, SSAExpr)): 
						addrKey = dep[0].addr.reg.num
						if( not addrKey in gadgetLookUp[GadgetType.MEMtoREG][reg.num]):
							gadgetLookUp[GadgetType.MEMtoREG][reg.num][addrKey] = [i]
						else:
							gadgetLookUp[GadgetType.MEMtoREG][reg.num][addrKey].append(i)
					# For MEMEXPRtoREG
					else:
						pass
				# FOR EXPRtoREG
				elif( dep[1].isTrue() ):
					if( reg.num in gadgetLookUp[GadgetType.EXPRtoREG] ):
						exprLookUpEXPRtoREG = gadgetLookUp[GadgetType.EXPRtoREG][reg.num]
					else:
						gadgetLookUp[GadgetType.EXPRtoREG][reg.num] = exprLookUp()
						exprLookUpEXPRtoREG = gadgetLookUp[GadgetType.EXPRtoREG][reg.num]
					exprLookUpEXPRtoREG.expr_list.append(dep[0])
					exprLookUpEXPRtoREG.gadget_list.append([i])
					
					
		for addr, deps in gadget.getDependencies().memDep.iteritems():
			# For REGtoMEM
			memLookUpREGtoMEM = gadgetLookUp[GadgetType.REGtoMEM]
			memLookUpREGtoMEM.addr_list.append(addr)
			memLookUpREGtoMEM.written_values.append(dict())
			
			# For CSTtoMEM
			memLookUpCSTtoMEM = gadgetLookUp[GadgetType.CSTtoMEM]
			memLookUpCSTtoMEM.addr_list.append(addr)
			memLookUpCSTtoMEM.written_values.append(dict())
			
			for dep in deps:
				# For REGtoMEM
				if( isinstance( dep[0], SSAExpr ) and dep[1].isTrue()):
					if( dep[0].reg.num in memLookUpREGtoMEM.written_values[-1]):
						memLookUpREGtoMEM.written_values[-1][dep[0].reg.num].append(i)	
					else:
						memLookUpREGtoMEM.written_values[len(memLookUpREGtoMEM.addr_list)-1][dep[0].reg.num] = [i]
				elif( isinstance(dep[0], ConstExpr) and dep[1].isTrue()):
					if( dep[0].value in memLookUpCSTtoMEM.written_values[-1]):
						memLookUpCSTtoMEM.written_values[-1][dep[0].value].append(i)
					else:
						memLookUpCSTtoMEM.written_values[-1][dep[0].value] = [i]
				# FOR THE REST --> IMPLEMENT LATER !! 
				else:
					pass
				
				
def pretty_print_registers():
	if( not gadgetDB ):
		print("You should generate gadgets before looking at the registers. Type 'load help' for help")
	else:
		print("\n\tRegisters present in the gadget database:")
		print("\t(Architeture is '" + ArchInfo.currentArch +"')\n")
		for reg in regNamesTable.keys():
			if( reg == ArchInfo.ip ):
				print('\t'+reg+ " (instruction pointer)")
			elif( reg == ArchInfo.sp ):
				print('\t'+reg+ " (stack pointer)")
			else:
				print('\t'+reg)

