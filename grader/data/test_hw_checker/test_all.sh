echo "SHOULD BE NO ERRORS:"
echo "csharp.tar.gz"
./check_hw.sh csharp.tar.gz
echo "c.tar.gz"
./check_hw.sh c.tar.gz
echo "c++.tar.gz"
./check_hw.sh c++.tar.gz
echo "fsharp.tar.gz"
./check_hw.sh fsharp.tar.gz
echo "fsharp2.tar.gz"
./check_hw.sh fsharp2.tar.gz
echo "java.tar.gz"
./check_hw.sh java.tar.gz
echo "java2.tar.gz"
./check_hw.sh java2.tar.gz
echo "jython.tar.gz"
./check_hw.sh jython.tar.gz
echo "php.tar.gz"
./check_hw.sh php.tar.gz
echo "pl.tar.gz"
./check_hw.sh pl.tar.gz
echo "py.tar.gz"
./check_hw.sh py.tar.gz
echo "java_folders.tar.gz"
./check_hw_folders.sh java_folders.tar.gz
echo "py_folders.tar.gz"
./check_hw_folders.sh py_folders.tar.gz
echo "nested_src_files.tar.gz"
./check_hw.sh nested_src_files.tar.gz
echo "code_src_in_folders.tar.gz"
./check_hw.sh code_src_in_folders.tar.gz
echo "java_multi_class.tar.gz"
./check_hw.sh java_multi_class.tar.gz
echo "java_multi_class_multi_code.tar.gz"
./check_hw.sh java_multi_class_multi_code.tar.gz
echo "MISSING CODE/SRC"
echo "no_code.tar.gz"
./check_hw.sh no_code.tar.gz
echo "no_src.tar.gz"
./check_hw.sh no_src.tar.gz
echo "MISSING PARTIAL CODE"
echo "c_h_missing.tar.gz"
./check_hw.sh c_h_missing.tar.gz
echo "MISSING FILES"
echo "missing_file1.tar.gz"
./check_hw.sh missing_file1.tar.gz
echo "missing_file2.tar.gz"
./check_hw.sh missing_file2.tar.gz
echo "missing_file_in_folder.tar.gz"
./check_hw_folders.sh missing_file_in_folder.tar.gz
echo "MISSING FOLDERS"
echo "missing_folder.tar.gz"
./check_hw_folders.sh missing_folder.tar.gz
echo "missing_folder2.tar.gz"
./check_hw_folders.sh missing_folder2.tar.gz
echo "missing_nested_folder.tar.gz"
./check_hw_folders.sh missing_nested_folder.tar.gz
echo "MISSING SHEBANG"
echo "no_shebang.tar.gz"
./check_hw.sh no_shebang.tar.gz
echo "no_shebang_nested.tar.gz"
./check_hw_folders.sh no_shebang_nested.tar.gz
echo "CORRUPTED TAR FILE"
echo "corrupted.tar.gz"
./check_hw.sh corrupted.tar.gz
echo "MULTIPLE ERRORS"
echo "missing_file_no_shebang.tar.gz"
./check_hw.sh missing_file_no_shebang.tar.gz
echo "missing_folder_missing_file.tar.gz"
./check_hw_folders.sh missing_folder_missing_file.tar.gz
echo "no_src_missing_file.tar.gz"
./check_hw.sh no_src_missing_file.tar.gz
echo "no_code_no_shebang.tar.gz"
./check_hw.sh no_code_no_shebang.tar.gz
echo "no_code_missing_file.tar.gz"
./check_hw.sh no_code_missing_file.tar.gz
echo "empty.tar.gz"
./check_hw.sh empty.tar.gz