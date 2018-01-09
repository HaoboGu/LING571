universe	= vanilla
executable	= $(script)
getenv		= true
output		= $(student)/condor.out
error		= $(student)/condor.err
log			= $(student)/condor.log
arguments	= "$(student)"
transfer_executable = false
queue
