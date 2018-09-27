import subprocess



valid_inputs = ["pause", "quit","seek 10","seek 10 0",
"seek -10 0", "seek -10"
]
while True:
	
	prompt_text = "Enter a command: "

	user =  raw_input (prompt_text)
	if(user in valid_inputs):
		subprocess.call("echo "+str(user)+" > video_fifo", shell=True)
		if(user == "quit"):
			quit()
	elif(user == "stop"):
		quit()
	else:
		print("Not valid command")
