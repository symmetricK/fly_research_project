from __future__ import print_function
import sys
#import trapcam_analysis_old as t
import trapcam_analysis as t

###dir = input("Enter the experiment directory you'd like to analyze (e.g. '2017_10_26'): ")
# dir = sys.argv[1]
dir='2017_10_26'


print ('')
while True:
    analyze_trap_list = []
###    letter = input("Enter a trap letter to analyze: ")
    letter="G"
###    letter="dummy"
##    letter="test"
#    letter="exp2_dummy_dummy"
    analyze_trap_list.append('trap_'+letter)
    while True:
###        letter = input("Enter another trap letter to analyze, or enter 'go' to start batch analysis: ")
        letter='go'
        if letter == 'go':
            break
        else:
            analyze_trap_list.append('trap_'+letter)
    print ('')
    print ('you said you want to analyze: ')
    for an_trap in analyze_trap_list:
        print (an_trap)
###    user_go_ahead = input("Are those the traps you'd like to analyze? (y/n) ")
        user_go_ahead='y'
    if user_go_ahead == 'y':
        break
    if user_go_ahead == 'n':
        continue
print ('')

calculate_threshold = False
calculate_final = False
###thresh_or_final = input("Do you want to analyze just a subset of frames to determine the best in-trap/on-trap threshold, or do you want to do the final analysis? (threshold/final) ")
thresh_or_final='final'

if thresh_or_final =='threshold':
    calculate_threshold = True
if thresh_or_final == 'final':
    calculate_final = True

for trap in analyze_trap_list:
    analyzer = t.TrapcamAnalyzer(dir, trap, calculate_threshold, calculate_final)
    analyzer.run()
