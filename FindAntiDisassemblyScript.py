#Script used to identify anti-disassembly techniques
#@author 
#@category _NEW_
#@keybinding 
#@menupath 
#@toolbar 



listing = currentProgram.getListing()
instr_list = listing.getInstructions(1)

for instr in instr_list:
	mnemonic = instr.getMnemonicString()

	# TODO: Add more constant idenitifiers
	# Looking for potential constant branches
	if mnemonic == "XOR":

		try:
			op1 = instr.getOpObjects(0)
			op2 = instr.getOpObjects(1)

			# Checks if zero flag is set
			if op1[0] == op2[0]:
				next_instr = instr.getNext()
				next_mnemonic = next_instr.getMnemonicString()

				# Checks if jump is being taken based on zero flag
				if next_mnemonic == "JZ" or next_mnemonic == "JE" or next_mnemonic == "JLE" or next_mnemonic == "JGE":
					addr = next_instr.getAddress()
					j_addr = next_instr.getOpObjects(0)[0]
					print("Constant branch condition at " + str(addr) + ". Jumps to " + str(j_addr))
		except:
			print("Constant branch error")
			pass

	# Multiple jumps to the same target
	elif mnemonic == "JZ" or mnemonic == "JNZ" or mnemonic == "JE" or mnemonic == "JNE":
		try:
			next_instr = instr.getNext()
			next_mnemonic = next_instr.getMnemonicString()
			if next_mnemonic == "JZ" or next_mnemonic == "JNZ" or next_mnemonic == "JE" or next_mnemonic == "JNE":
				j_addr1 = instr.getOpObjects(0)[0]
				j_addr2 = next_instr.getOpObjects(0)[0]

				if j_addr1 == j_addr2 and (((mnemonic == "JZ" or mnemonic == "JE") and (next_mnemonic == "JNZ" or next_mnemonic == "JNE")) or ((mnemonic == "JNZ" or mnemonic == "JNE") and (next_mnemonic == "JZ" or next_mnemonic == "JE"))):
					addr = instr.getAddress()
					print("Multiple jumps to same target at " + str(addr) + ". Jumps to " + str(j_addr1))

		except:
			print("Same target error")
			pass

	# Impossible disassembly
	elif mnemonic == "JMP" and getInstructionAt(instr.getOpObjects(0)[0]) is None:
		try:
			valid_addr = getDataAt(instr.getOpObjects(0)[0]).isPointer()
		except:
			valid_addr = False

		if not valid_addr:
			addr = instr.getAddress()
			j_addr = instr.getOpObjects(0)[0]
			print("Jump to impossible disassembly segment at " + str(addr) + ". Jumps to " + str(j_addr))