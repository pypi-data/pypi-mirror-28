import timeit

code = """
# consensus = _quickconsensus.MismatchCounts("4", 96549060, 96549060+1000)
# consensus = quickconsensus.MismatchCounts("4", 96549060, 96549060+1000)
consensus = _quickconsensus.MismatchCounts("4", 96549060, 96567077)
# consensus = quickconsensus.MismatchCounts("4", 96549060, 96567077)
consensus.tally_reads(bam)
# print(consensus.counts)
"""

setup = """
import pysam

import pyximport; pyximport.install()
import _quickconsensus

bam = pysam.AlignmentFile("../test/quick_consensus_test.bam")
"""

times = timeit.repeat(code, setup, number=1, repeat=3)

import numpy

print(f"{numpy.mean(times):.2f}+/-{numpy.std(times):.2f}s")