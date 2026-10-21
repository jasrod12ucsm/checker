# Pruebas del checker: un .cpp por regla con // expected-warning{{…}} (-verify).
import os
import lit.formats

config.name = "ucsm-container-invalidation"
config.test_format = lit.formats.ShTest(True)
config.suffixes = [".cpp"]
config.test_source_root = os.path.dirname(__file__)
config.test_exec_root = os.path.join(os.path.dirname(config.plugin), "tests", "lit")
config.excludes = ["Inputs"]

analyze = (f"{config.llvm_bin}/clang++ -std=c++17 --analyze -o /dev/null "
           f"-Xclang -load -Xclang {config.plugin} "
           f"-Xclang -analyzer-checker=ucsm.ContainerInvalidation "
           f"-Xclang -verify")
config.substitutions.append(("%analyze", analyze))
config.substitutions.append(("%possibly",
    "-Xclang -analyzer-config -Xclang ucsm.ContainerInvalidation:PolicyMode=Possibly"))
config.environment["PATH"] = config.llvm_bin + os.pathsep + os.environ.get("PATH", "")
config.substitutions.append(("%clang", f"{config.llvm_bin}/clang"))
config.substitutions.append(("%plugin", config.plugin))
