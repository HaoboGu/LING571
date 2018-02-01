executable = hw4_run.sh
getenv     = true
log        = hw4.log
error      = hw4.err
notification = never
arguments  = "data/parses.train hw4_base.pcfg data/sentences.txt parses_base.out hw4_improved.pcfg parses_improved.out parses_base.eval parses_improved.eval"
transfer_executable = false
request_memory = 2*1024
queue

