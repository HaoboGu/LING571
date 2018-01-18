executable = hw1_parse.sh
getenv     = true
log        = log
error      = err
notification = never
arguments  = "../hw2/atis.cfg ../hw2/sentences.txt ../hw2/hw2_orig_output.txt"
transfer_executable = false
request_memory = 2*1024
queue

executable = hw1_parse.sh
getenv     = true
log        = log2
error      = err2
notification = never
arguments  = "../hw2/hw2_grammar_cnf.cfg ../hw2/sentences.txt ../hw2/hw2_cnf_output.txt"
transfer_executable = false
request_memory = 2*1024
queue
