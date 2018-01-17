executable = hw2_tocnf.sh
getenv     = true
notification = complete
arguments  = "atis.cfg hw2_grammar_cnf.cfg"
transfer_executable = false
request_memory = 2*1024
queue

executable = hw1_parse.sh
getenv     = true
notification = complete
arguments  = "atis.cfg sentences.txt hw2_orig_output.txt"
transfer_executable = false
request_memory = 2*1024
queue

executable = hw1_parse.sh
getenv     = true
notification = complete
arguments  = "hw2_grammar_cnf.cfg sentences.txt hw2_cnf_output.txt"
transfer_executable = false
request_memory = 2*1024
queue
