CXX = g++
CXX_FLAGS = -std=c++20
WARN_FLAGS = -Wall -Wextra -pedantic
OPT_FLAGS = -O3 -march=native -mtune=native
IFLAGS = -I ./include
DEP_IFLAGS = -I ./subtle/include
PERF_DEFS = -DCYCLES_PER_BYTE -DINSTRUCTIONS_PER_CYCLE

all: test

tests/test_ascon_perm.o: tests/test_ascon_perm.cpp include/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

tests/test_ascon128_aead.o: tests/test_ascon128_aead.cpp include/*.hpp include/aead/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

tests/test_ascon128a_aead.o: tests/test_ascon128a_aead.cpp include/*.hpp include/aead/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

tests/test_ascon80pq_aead.o: tests/test_ascon80pq_aead.cpp include/*.hpp include/aead/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

tests/test_ascon_hash.o: tests/test_ascon_hash.cpp include/*.hpp include/hashing/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

tests/test_ascon_hasha.o: tests/test_ascon_hasha.cpp include/*.hpp include/hashing/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

tests/test_ascon_xof.o: tests/test_ascon_xof.cpp include/*.hpp include/hashing/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

tests/test_ascon_xofa.o: tests/test_ascon_xofa.cpp include/*.hpp include/hashing/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

tests/test_ascon_prf.o: tests/test_ascon_prf.cpp include/*.hpp include/auth/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

tests/test_ascon_mac.o: tests/test_ascon_mac.cpp include/*.hpp include/auth/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

tests/test_ascon_prfs.o: tests/test_ascon_prfs.cpp include/*.hpp include/auth/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

tests/a.out: tests/test_ascon_perm.o \
				tests/test_ascon128_aead.o tests/test_ascon128a_aead.o tests/test_ascon80pq_aead.o \
					tests/test_ascon_hash.o tests/test_ascon_hasha.o tests/test_ascon_xof.o tests/test_ascon_xofa.o \
						tests/test_ascon_prf.o tests/test_ascon_mac.o tests/test_ascon_prfs.o
	$(CXX) $(OPT_FLAGS) $^ -lgtest -lgtest_main -o $@

test: tests/a.out
	./$<

benchmarks/bench_ascon_perm.o: benchmarks/bench_ascon_perm.cpp include/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

benchmarks/perf_ascon_perm.o: benchmarks/bench_ascon_perm.cpp include/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) $(PERF_DEFS) -c $< -o $@

benchmarks/bench_ascon128_aead.o: benchmarks/bench_ascon128_aead.cpp include/*.hpp include/aead/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

benchmarks/perf_ascon128_aead.o: benchmarks/bench_ascon128_aead.cpp include/*.hpp include/aead/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) $(PERF_DEFS) -c $< -o $@

benchmarks/bench_ascon128a_aead.o: benchmarks/bench_ascon128a_aead.cpp include/*.hpp include/aead/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

benchmarks/perf_ascon128a_aead.o: benchmarks/bench_ascon128a_aead.cpp include/*.hpp include/aead/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) $(PERF_DEFS) -c $< -o $@

benchmarks/bench_ascon80pq_aead.o: benchmarks/bench_ascon80pq_aead.cpp include/*.hpp include/aead/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

benchmarks/perf_ascon80pq_aead.o: benchmarks/bench_ascon80pq_aead.cpp include/*.hpp include/aead/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) $(PERF_DEFS) -c $< -o $@

benchmarks/bench_ascon_hash.o: benchmarks/bench_ascon_hash.cpp include/*.hpp include/hashing/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

benchmarks/perf_ascon_hash.o: benchmarks/bench_ascon_hash.cpp include/*.hpp include/hashing/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) $(PERF_DEFS) -c $< -o $@

benchmarks/bench_ascon_hasha.o: benchmarks/bench_ascon_hasha.cpp include/*.hpp include/hashing/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

benchmarks/perf_ascon_hasha.o: benchmarks/bench_ascon_hasha.cpp include/*.hpp include/hashing/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) $(PERF_DEFS) -c $< -o $@

benchmarks/bench_ascon_xof.o: benchmarks/bench_ascon_xof.cpp include/*.hpp include/hashing/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

benchmarks/perf_ascon_xof.o: benchmarks/bench_ascon_xof.cpp include/*.hpp include/hashing/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) $(PERF_DEFS) -c $< -o $@

benchmarks/bench_ascon_xofa.o: benchmarks/bench_ascon_xofa.cpp include/*.hpp include/hashing/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

benchmarks/perf_ascon_xofa.o: benchmarks/bench_ascon_xofa.cpp include/*.hpp include/hashing/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) $(PERF_DEFS) -c $< -o $@

benchmarks/bench_ascon_prf.o: benchmarks/bench_ascon_prf.cpp include/*.hpp include/auth/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

benchmarks/perf_ascon_prf.o: benchmarks/bench_ascon_prf.cpp include/*.hpp include/auth/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) $(PERF_DEFS) -c $< -o $@

benchmarks/bench_ascon_mac.o: benchmarks/bench_ascon_mac.cpp include/*.hpp include/auth/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

benchmarks/perf_ascon_mac.o: benchmarks/bench_ascon_mac.cpp include/*.hpp include/auth/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) $(PERF_DEFS) -c $< -o $@

benchmarks/bench_ascon_prfs.o: benchmarks/bench_ascon_prfs.cpp include/*.hpp include/auth/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) -c $< -o $@

benchmarks/perf_ascon_prfs.o: benchmarks/bench_ascon_prfs.cpp include/*.hpp include/auth/*.hpp
	$(CXX) $(CXX_FLAGS) $(WARN_FLAGS) $(OPT_FLAGS) $(IFLAGS) $(DEP_IFLAGS) $(PERF_DEFS) -c $< -o $@

benchmarks/bench.out: benchmarks/bench_ascon_perm.o \
						benchmarks/bench_ascon128_aead.o benchmarks/bench_ascon128a_aead.o benchmarks/bench_ascon80pq_aead.o \
							benchmarks/bench_ascon_hash.o benchmarks/bench_ascon_hasha.o benchmarks/bench_ascon_xof.o benchmarks/bench_ascon_xofa.o \
								benchmarks/bench_ascon_prf.o benchmarks/bench_ascon_mac.o benchmarks/bench_ascon_prfs.o
	# In case you haven't built google-benchmark with libPFM support.
	# More @ https://gist.github.com/itzmeanjan/05dc3e946f635d00c5e0b21aae6203a7
	$(CXX) $(OPT_FLAGS) $^ -lbenchmark -lbenchmark_main -lpthread -o $@

benchmarks/perf.out: benchmarks/perf_ascon_perm.o \
						benchmarks/perf_ascon128_aead.o benchmarks/perf_ascon128a_aead.o benchmarks/perf_ascon80pq_aead.o \
							benchmarks/perf_ascon_hash.o benchmarks/perf_ascon_hasha.o benchmarks/perf_ascon_xof.o benchmarks/perf_ascon_xofa.o \
								benchmarks/perf_ascon_prf.o benchmarks/perf_ascon_mac.o benchmarks/perf_ascon_prfs.o
	# In case you've built google-benchmark with libPFM support.
	# More @ https://gist.github.com/itzmeanjan/05dc3e946f635d00c5e0b21aae6203a7
	$(CXX) $(OPT_FLAGS) $^ -lbenchmark -lbenchmark_main -lpthread -lpfm -o $@

bench: benchmarks/bench.out
	./$< --benchmark_counters_tabular=true --benchmark_min_warmup_time=1.

perf: benchmarks/perf.out
	./$< --benchmark_counters_tabular=true --benchmark_min_warmup_time=1. --benchmark_perf_counters=CYCLES,INSTRUCTIONS

clean:
	find . -name '*.out' -o -name '*.o' -o -name '*.gch' | xargs rm -rf

format:
	find include/ benchmarks/ tests/ -name '*.hpp' -o -name '*.cpp' | xargs clang-format -i
