import sys
import os
import subprocess


if __name__ == "__main__":
    use_local_file = True
    if use_local_file:
        # print(os.listdir())
        if 'hw4' in os.listdir():
            os.chdir('hw4')
        treebank_filename = 'data/parses.train'
        output_pcfg_filename = "hw4_base.pcfg"
        sentences_filename = 'data/sentences.txt'
        baseline_parses_filename = "parses_base.out"
        input_pcfg_filename = 'hw4_improved.pcfg'
        improved_parses_filename = "parses_improved.out"
        baseline_eval = 'parses_base.eval'
        improved_eval = "parses_improved.eval"
    else:
        treebank_filename = sys.argv[1]
        output_pcfg_filename = sys.argv[2]
        sentences_filename = sys.argv[3]
        baseline_parses_filename = sys.argv[4]
        input_pcfg_filename = sys.argv[5]
        improved_parses_filename = sys.argv[6]
        baseline_eval = sys.argv[7]
        improved_eval = sys.argv[8]

    gold_standard_filename = 'data/parses.gold'
    if 'tools' in os.listdir():
        # command for evaluating baseline system
        command3 = ['tools/evalb', '-p', 'tools/COLLINS.prm', gold_standard_filename, baseline_parses_filename]
        # command for evaluating improved system
        command6 = ['tools/evalb', '-p', 'tools/COLLINS.prm', gold_standard_filename, improved_parses_filename]
    else:
        # command for evaluating baseline system
        command3 = ['./evalb', '-p', './COLLINS.prm', gold_standard_filename, baseline_parses_filename]
        # command for evaluating improved system
        command6 = ['./evalb', '-p', './COLLINS.prm', gold_standard_filename, improved_parses_filename]

    # command for converting treebank to pcfg
    command1 = ['./hw4_topcfg.sh', treebank_filename, output_pcfg_filename]
    # command for basic parsing
    command2 = ['./hw4_parser.sh', output_pcfg_filename, sentences_filename, baseline_parses_filename]
   # command for converting treebank to pcfg improved version
    command4 = ['./hw4_improved_induction.sh', treebank_filename, input_pcfg_filename]
    # command for improved parsing
    command5 = ['./hw4_improved_parser.sh', input_pcfg_filename, sentences_filename, improved_parses_filename]

    subprocess.call(command1)
    subprocess.call(command2)
    subprocess.call(command3)
    subprocess.call(command4)
    subprocess.call(command5)
    subprocess.call(command6)




