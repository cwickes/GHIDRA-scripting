#Script used to identify anti-disassembly techniques
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 



listing = currentProgram.getListing()
instr_list = listing.getInstructions(1)

for instr in instr_list:
	# Looking for potential constant branches
	if instr.getMnemonicString() == "XOR":

		try:
			op1 = instr.getOpObjects(0)
			op2 = instr.getOpObjects(1)

			# Checks if zero flag is set
			if op1[0] == op2[0]:
				next_instr = instr.getNext()
				next_mnemonic = next_instr.getMnemonicString()

				# Checks if jump is being taken based on zero flag
				if next_mnemonic == "JZ" or next_mnemonic == "JE":
					addr = next_instr.getAddress()
					j_addr = next_instr.getOpObjects(0)[0]
					print("Constant branch condition at " + str(addr) + ". Jumps to " + str(j_addr))
		except:
			print("ERROR")
			pass