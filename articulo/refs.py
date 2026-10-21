"""Inserta la lista de referencias (IEEE Reference Guide V 3.28.2025) en el orden de la primera cita."""
import re, sys
ACC = "Accessed: Oct. 20, 2026."
R = {
"iso17": r"\textit{Programming Languages---C++}, ISO/IEC Standard 14882:2017, Int. Org. Standardization, Geneva, Switzerland, Dec. 2017.",
"cert": r"Software Eng. Inst. ``CTR51-CPP. Use valid references, pointers, and iterators to reference elements of a container.'' SEI CERT C++ Coding Standard. " + ACC + r" [Online]. Available: \url{https://wiki.sei.cmu.edu/confluence/spaces/cplusplus/pages/88046457/CTR51-CPP.+Use+valid+references+pointers+and+iterators+to+reference+elements+of+a+container}",
"landi92": r"W. Landi, ``Undecidability of static analysis,'' \textit{ACM Lett. Program. Lang. Syst.}, vol. 1, no. 4, pp. 323--337, Dec. 1992, doi: 10.1145/161494.161501.",
"ramalingam94": r"G. Ramalingam, ``The undecidability of aliasing,'' \textit{ACM Trans. Program. Lang. Syst.}, vol. 16, no. 5, pp. 1467--1471, Sep. 1994, doi: 10.1145/186025.186041.",
"livshits15": r"B. Livshits \textit{et al.}, ``In defense of soundiness: A manifesto,'' \textit{Commun. ACM}, vol. 58, no. 2, pp. 44--46, Feb. 2015, doi: 10.1145/2644805.",
"christakis16": r"M. Christakis and C. Bird, ``What developers want and need from program analysis: An empirical study,'' in \textit{Proc. 31st IEEE/ACM Int. Conf. Automated Softw. Eng. (ASE)}, Singapore, Sep. 2016, pp. 332--343, doi: 10.1145/2970276.2970347.",
"guo23": r"Z. Guo \textit{et al.}, ``Mitigating false positive static analysis warnings: Progress, challenges, and opportunities,'' \textit{IEEE Trans. Softw. Eng.}, vol. 49, no. 12, pp. 5154--5188, Dec. 2023, doi: 10.1109/TSE.2023.3329667.",
"king76": r"J. C. King, ``Symbolic execution and program testing,'' \textit{Commun. ACM}, vol. 19, no. 7, pp. 385--394, Jul. 1976, doi: 10.1145/360248.360252.",
"csadev": r"LLVM Project. ``Checker developer manual.'' Clang Static Analyzer. " + ACC + r" [Online]. Available: \url{https://clang-analyzer.llvm.org/checker_dev_manual.html}",
"csadoc": r"LLVM Project. ``Available checkers.'' Clang Static Analyzer Documentation. " + ACC + r" [Online]. Available: \url{https://clang.llvm.org/docs/analyzer/checkers.html}",
"balogh18": r"\'{A}. Balogh. (Apr. 2018). \textit{Finding iterator-related errors with Clang Static Analyzer}. Presented at EuroLLVM 2018, Bristol, U.K. [Online]. Available: \urlbalogh",
"saxena26": r"U. Saxena. \textit{[LifetimeSafety] Detect Use-After-Invalidation for STL Containers}. (Feb. 6, 2026). GitHub: llvm/llvm-project, Pull Request 179093, commit 21f3875. " + ACC + r" [Online]. Available: \url{https://github.com/llvm/llvm-project/pull/179093}",
"infer": r"Meta Platforms. ``List of all issue types.'' Infer. " + ACC + r" [Online]. Available: \url{https://fbinfer.com/docs/all-issue-types/}",
"cppcheck": r"Cppcheck Team. \textit{Cppcheck: lib/checkstl.cpp}. (Sep. 19, 2026). GitHub: danmar/cppcheck. (v2.22.0). " + ACC + r" [Online]. Available: \url{https://github.com/danmar/cppcheck/blob/2.22.0/lib/checkstl.cpp}",
"liu25": r"S. Liu, L. Chen, G. Fan, B. Yin, C. Huang, and J. Wang, ``Detecting vector container errors in C++ programs via abstract interpretation,'' in \textit{Proc. 26th Int. Conf. Formal Eng. Methods (ICFEM)}, in Lecture Notes Comput. Sci., vol. 16229, Hangzhou, China, Nov. 2025, pp. 117--133, doi: 10.1007/978-981-95-4213-0\_7.",
"sutter19": r"H. Sutter, ``Lifetime safety: Preventing common dangling,'' ISO/IEC JTC1/SC22/WG21, Geneva, Switzerland, Rep. P1179R1, Nov. 22, 2019. [Online]. Available: \url{https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1179r1.pdf}",
"rust23": r"S. Klabnik and C. Nichols, \textit{The Rust Programming Language}, 2nd ed. San Francisco, CA, USA: No Starch Press, 2023.",
"cousot77": r"P. Cousot and R. Cousot, ``Abstract interpretation: A unified lattice model for static analysis of programs by construction or approximation of fixpoints,'' in \textit{Proc. 4th ACM SIGACT-SIGPLAN Symp. Princ. Program. Lang. (POPL)}, Los Angeles, CA, USA, Jan. 1977, pp. 238--252, doi: 10.1145/512950.512973.",
"higgs20": r"K. Higgs, ``Detecting iterator invalidation with CodeQL,'' \textit{Trail of Bits Blog}, Oct. 9, 2020. [Online]. Available: \url{https://blog.trailofbits.com/2020/10/09/detecting-iterator-invalidation-with-codeql/}",
"pvs": r"PVS-Studio. ``V789. Iterators for the container, used in the range-based for loop, become invalid upon a function call.'' PVS-Studio Documentation. " + ACC + r" [Online]. Available: \url{https://pvs-studio.com/en/docs/warnings/v789/}",
"teodorescu24": r"V.-A. Teodorescu and D. Lucanu, ``Static analysis framework for detecting use-after-free bugs in C++,'' \textit{Electron. Proc. Theor. Comput. Sci.}, vol. 410, pp. 99--115, Oct. 2024, doi: 10.4204/EPTCS.410.7.",
"libstdcxx": r"GNU Project. ``Chapter 18. Debug mode.'' The GNU C++ Library Manual. " + ACC + r" [Online]. Available: \url{https://gcc.gnu.org/onlinedocs/libstdc++/manual/debug_mode.html}",
"asan": r"LLVM Project. ``AddressSanitizer.'' Clang Documentation. " + ACC + r" [Online]. Available: \url{https://clang.llvm.org/docs/AddressSanitizer.html}",
"kashyap19": r"V. Kashyap \textit{et al.}, ``Automated customized bug-benchmark generation,'' in \textit{Proc. IEEE 19th Int. Work. Conf. Source Code Anal. Manipulation (SCAM)}, Cleveland, OH, USA, Sep. 2019, pp. 103--114, doi: 10.1109/SCAM.2019.00020.",
"klinger19": r"C. Klinger, M. Christakis, and V. W\"{u}stholz, ``Differentially testing soundness and precision of program analyzers,'' in \textit{Proc. 28th ACM SIGSOFT Int. Symp. Softw. Testing Anal. (ISSTA)}, Beijing, China, Jul. 2019, pp. 239--250, doi: 10.1145/3293882.3330553.",
"n4659": r"R. Smith, ``Working draft, standard for programming language C++,'' ISO/IEC JTC1/SC22/WG21, Geneva, Switzerland, Rep. N4659, Mar. 21, 2017. [Online]. Available: \url{https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2017/n4659.pdf}",
"lattner04": r"C. Lattner and V. Adve, ``LLVM: A compilation framework for lifelong program analysis \& transformation,'' in \textit{Proc. Int. Symp. Code Gener. Optim. (CGO)}, San Jose, CA, USA, Mar. 2004, pp. 75--86, doi: 10.1109/CGO.2004.1281665.",
"sarif": r"\textit{Static Analysis Results Interchange Format (SARIF) Version 2.1.0}, OASIS Standard sarif-v2.1.0-os, Mar. 27, 2020. [Online]. Available: \url{https://docs.oasis-open.org/sarif/sarif/v2.1.0/os/sarif-v2.1.0-os.html}",
}
src = open(sys.argv[1]).read()
body = src.split(r"\begin{thebibliography}")[0]
orden = []
for grupo in re.findall(r"\\cite\{([^}]*)\}", body):
    for k in grupo.split(","):
        k = k.strip()
        if k not in orden:
            orden.append(k)
faltan = [k for k in orden if k not in R]
sobran = [k for k in R if k not in orden]
# --solo-citadas: versiones parciales del artículo, que citan un subconjunto
if faltan or (sobran and "--solo-citadas" not in sys.argv):
    sys.exit(f"faltan {faltan}, sin citar {sobran}")
items = "\n".join(f"\\bibitem{{{k}}} {R[k]}" for k in orden)
out = re.sub(r"\\begin\{thebibliography\}\{00\}.*?\\end\{thebibliography\}",
             lambda _: "\\begin{thebibliography}{00}\n" + items + "\n\\end{thebibliography}", src, flags=re.S)
open(sys.argv[2], "w").write(out)
print(len(orden), "referencias")
